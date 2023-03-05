from email.policy import default
from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)

    class Config:
        schema_extra = {
            "post_demo" : {
                "title" : "some title about animals",
                "content" : "some content about animals"
            }
        }

class UserSchema(BaseModel):
    full_name : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)

    class Config:
        schema = {
            "user_demo" : {
                "name" : "full name",
                "email" : "email@example.com",
                "password" : "password"
            }
        }


class LoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)

    class Config:
        schema = {
            "user_demo" : {
                "email" : "email@example.com",
                "password" : "password"
            }
        }