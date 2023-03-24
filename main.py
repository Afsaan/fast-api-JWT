import os
import csv
import pandas as pd
import joblib


from fastapi import Body, FastAPI, Depends, HTTPException, Request, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.models import UserSchema, LoginSchema, ModelSchema, PayloadSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from app.train import train_model

from constant import DATA_DIR_NAME, USER_DATA_PATH, TRAIN_DATA_PATH, MODEL_DIR_PATH, MODEL_PATH


#load the model
model = joblib.load(f"{MODEL_DIR_PATH}/{MODEL_PATH}")
app = FastAPI()

# @app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  
    errors = []
    for error in exc.errors():
        error_msg = error["msg"]
        field = error["loc"][0]
        errors.append({field: error_msg})
    return JSONResponse(content={"detail": errors, "body": error["ctx"]["doc"] }, status_code=400)

#basic home page
@app.get("/", tags = ["Greet"])
def Welcome():
    return {"Hello": "Welcome to HeathCare page"}

# add the data to csv and predictions
@app.post("/predict", dependencies = [Depends(jwtBearer())], tags = ["predictions"])
def get_post(value: ModelSchema):
    data = [values for values in value.dict().values()]

    if not os.path.exists(DATA_DIR_NAME):
        os.makedirs(DATA_DIR_NAME)

    # predict the output
    result = model.predict([data])

    #appending in data
    data.append(int(result[0]))

    with open(f"{DATA_DIR_NAME}/{TRAIN_DATA_PATH}", 'a', newline='') as f:
        # create a csv.writer object
        writer = csv.writer(f)
        # write data into the CSV file
        writer.writerows([data])

    if result[0] == 1:
        return {"data": "person is Diabatic"}

    return {"data": "person is NOT Diabatic"}

@app.get("/train", dependencies = [Depends(jwtBearer())], tags = ["train"])
def train_model():
    train_data = pd.read_csv(f"{DATA_DIR_NAME}/{TRAIN_DATA_PATH}")
    try:
        train_model(train_data)
    except Exception as msg:
        return {"data": f"Error due to : {msg}"}
    return {"data": "Model Trained SuccessFully"}


@app.post("/user/register" , tags = ["user"])
def register(user : UserSchema):

    if not user.email:
        raise HTTPException(status_code=422, detail="Missing email field")
    if not user.password:
        raise HTTPException(status_code=422, detail="Missing password field")
    
    data = [values for values in user.dict().values()]
    print(data)
    #check if file is present or not
    if not os.path.exists(DATA_DIR_NAME):
        os.makedirs(DATA_DIR_NAME)

    with open(f"{DATA_DIR_NAME}/{USER_DATA_PATH}", 'a', newline='') as f:
        # create a csv.writer object
        writer = csv.writer(f)
        # write data into the CSV file
        writer.writerows([data])

    return {"data": "Registered Successfully"}


def check_user(data: LoginSchema, user_db):
    for users in user_db.itertuples():
        if users.password == data.password and users.username == data.email:
            return True
    
    return False

@app.post("/user/login", tags = ["user"])
def user_login(user : LoginSchema = Body()):

    #load the csv file for user data
    user_db = pd.read_csv(f'{DATA_DIR_NAME}/{USER_DATA_PATH}')

    # check if user is already regstered or not
    if check_user(user, user_db):
        return signJWT(user.email)

    return {"data" : "User does not exist or invalid login details"}

@app.post('/payload')
async def handle_payload(payload: PayloadSchema , meta_transid: str = Header(name="meta-transid"), 
                            meta_src_envrmt:str = Header(name="meta-src-envrmt")):
    try:
        # process the payload here
        return {'message': 'success'}
    except ValueError as e:
        print('Error processing payload')
        raise HTTPException(status_code=400, detail=str(e))