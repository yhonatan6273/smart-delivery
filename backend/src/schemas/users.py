from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import  Optional




#this schema is for creating a new user and the information we get
class UserCreate(BaseModel):
    email:EmailStr
    password:str



#this schema is the information we return when we get user info
class UserOutput(BaseModel):
    id:int
    email:EmailStr
    role:str
    created_at:datetime



    class Config:
        from_attributes = True



#we enter email and password to login
class UserLogin(BaseModel):
    email:EmailStr
    password:str


#the output from login (we will receive a token)
class Token(BaseModel):
    access_token: str
    token_type: str


#this schema contains the data extracted from the token
class TokenData(BaseModel):
    id:Optional[str]=None
    role:Optional[str] = None


