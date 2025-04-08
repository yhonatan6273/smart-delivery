from datetime import datetime

from pydantic import BaseModel,Field,EmailStr
from typing import  Literal
from backend.Models import models


class DeliveryBase(BaseModel):
    sender_phone:str=Field(...,pattern=r'^\+?\d{10,15}$',title="phone number",examples=["+254712345678","+254712345678"])
    sender_id:str=Field(...,pattern=r'^\d{7,11}$',title="id",examples=["123456789","1234567890"])
    sender_name:str=Field(...,min_length=2,max_length=100)
    sender_address: str = Field(..., min_length=2, max_length=100)
    receiver_phone: str = Field(...,pattern=r'^\+?\d{10,15}$',title="phone number",examples=["+254712345678","+254712345678"])
    receiver_id:str=Field(...,pattern=r'^\d{7,11}$',title="id",examples=["123456789","1234567890"])
    receiver_name:str=Field(...,min_length=2,max_length=100)
    receiver_address:str=Field(...,min_length=2,max_length=100)
    status: Literal["delivered", "in-transit", "approve"] = Field(..., examples=["delivered", "in-transit", "approve"])
    price: float = Field(...,gt=0) #price have to be positive and bigger then 0
    delivery_type:str=Field(...,min_length=2,max_length=100)


class DeliveryCreate(DeliveryBase):
    pass

class DeliveryUpdate(BaseModel):
    status: Literal["delivered", "in-transit", "approve"] = Field(..., examples=["delivered", "in-transit", "approve"])



class DeliveryPostGetOutput(BaseModel):
    id:int
    delivery_type: str
    sender_phone:str
    sender_name: str
    sender_address: str
    receiver_address:str
    receiver_name:str
    receiver_phone:str
    status:str
    price:float
    time_of_created: datetime


    class Config:
        from_attributes = True

class DeliveryPutOutput(BaseModel):
    id:int
    delivery_type:str
    status:str
    time_of_created:datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserOutput(BaseModel):
    id:int
    email:EmailStr
    time_of_created:datetime

    class Config:
        from_attributes = True


