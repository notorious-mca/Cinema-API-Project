from typing import Optional
from pydantic import BaseModel,EmailStr


# User creation basic schema
class UserCreate(BaseModel):
    username: str
    email : EmailStr
    password : str


# Schema for hiding sensible information from post requests on "/users" endpoint
class ShowUser(BaseModel):
    username : str 
    email : EmailStr
    is_active : bool

    class Config():  #tells pydantic to convert even non dict obj to json
        orm_mode = True