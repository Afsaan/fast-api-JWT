from email.policy import default
from pydantic import BaseModel, Field, EmailStr

class ModelSchema(BaseModel):
    preg : int = Field(default=None)
    plas : int = Field(default=None)
    pressure : int = Field(default=None)
    skin : int = Field(default=None)
    test : int = Field(default=None)
    mass : int = Field(default=None)
    pedi : int = Field(default=None)
    age : int = Field(default=None)

    class Config:
        schema_extra = {
            "independent_variable" : {
                "preg" : 1,
                "plas" : 1,
                "pressure" : 1,
                "skin" : 1,
                "test" : 1,
                "mass" : 1,
                "pedi" : 1,
                "age" : 1,
            }
        }

class UserSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)

    class Config:
        schema = {
            "user_demo" : {
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