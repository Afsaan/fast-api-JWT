from fastapi import FastAPI
from app.models import PostSchema

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


@app.post("/posts", tags = ["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.apend(post.dict())

    return {"data": "Post Added SuccessFully"}
