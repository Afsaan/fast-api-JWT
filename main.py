from fastapi import Body, FastAPI, Depends
from app.models import PostSchema, UserSchema, LoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id" : 1,
        "title" : "panda",
        "content" : "lazy animals"
    },

    {
        "id" : 2,
        "title" : "elephant",
        "content" : "big animals"
    },

]

users = []

app = FastAPI()


#basic home page
@app.get("/", tags = ["Greet"])
def get_post():
    return {"Hello": "Welcome to post page"}


# get
@app.get("/posts", tags = ["posts"])
def get_post():
    return {"data": posts}

@app.get("/post/{id}" , tags = ["posts"])
def get_one_post(id : int):
    if id > len(posts):
        return {"error": "post with the id does not exist"}

    for post in posts:
        if post["id"] == id:
            return {"data": post}


@app.post("/posts", dependencies = [Depends(jwtBearer())], tags = ["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())

    return {"data": "Post Added SuccessFully"}


@app.post("/user/register" , tags = ["user"])
def register(user : UserSchema):
    users.append(user.dict())

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