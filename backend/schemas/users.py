from datetime import datetime
from pydantic import BaseModel,EmailStr
from typing import  Optional





class UserCreate(BaseModel):
    email:EmailStr
    password:str




class UserOutput(BaseModel):
    id:int
    email:EmailStr
    role:str
    time_of_created:datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id:Optional[str]=None


