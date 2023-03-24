from email.policy import default
from pydantic import BaseModel, Field, EmailStr, validator

class PayloadSchema(BaseModel):
    adhoc: bool
    analyticid: str
    hints: list[str]
    payload: dict

    @validator('hints')
    def options_validator(cls, values):
        allowed_values = ['cca','cc']
        for value in values:
            if value not in allowed_values:
                raise ValueError(f'Invalid option: {value}. Allowed values are {allowed_values}.')
        return values

    @validator('adhoc')
    def bool_validator(cls, values):
        if not values:
            raise ValueError('is_active must be a True')
        return values

    @validator('payload')
    def dict_validator(cls, values):
        if not isinstance(values, dict):
            raise ValueError('payload must be a dict data')
        return values

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