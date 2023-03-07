import os
import csv
import pandas as pd
import joblib


from fastapi import Body, FastAPI, Depends

from app.models import PostSchema, UserSchema, LoginSchema, ModelSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

from constant import DATA_DIR_NAME, USER_DATA_PATH, TRAIN_DATA_PATH, MODEL_DIR_PATH, MODEL_PATH


#load the model
model = joblib.load(f"{MODEL_DIR_PATH}/{MODEL_PATH}")

users = []

app = FastAPI()

#basic home page
@app.get("/", tags = ["Greet"])
def get_post():
    return {"Hello": "Welcome to post page"}


# add the data to csv and predictions
@app.get("/predict", dependencies = [Depends(jwtBearer())], tags = ["predictions"])
def get_post(value: ModelSchema):
    data = [values for values in value.dict().values()]

    if not os.path.exists(DATA_DIR_NAME):
        os.makedirs(DATA_DIR_NAME)

    with open(f"{DATA_DIR_NAME}/{TRAIN_DATA_PATH}", 'a', newline='') as f:
        # create a csv.writer object
        writer = csv.writer(f)
        # write data into the CSV file
        writer.writerows([data])
    
    # predict the output
    result = model.predict([data])
    if result[0] == 1:
        return {"data": "person is Diabatic"}
    
    return {"data": "person is NOT Diabatic"}

@app.post("/train", dependencies = [Depends(jwtBearer())], tags = ["train"])
def add_post(post : PostSchema):
    pass
    return {"data": "Model Trained SuccessFully"}


@app.post("/user/register" , tags = ["user"])
def register(user : UserSchema):
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


def check_user(data: LoginSchema):
    for user in users:
        print(user['password'] , data.password)
        if user['password'] == data.password and user['email'] == data.email:
            return True
    
    return False

@app.post("/user/login", tags = ["user"])
def user_login(user : LoginSchema = Body(default=None)):

    # check if user is already regstered or not
    if check_user(user):
        return signJWT(user.email)

    return {"data" : "User does not exist or invalid login details"}