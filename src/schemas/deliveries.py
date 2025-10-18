from datetime import datetime
from pydantic import BaseModel,Field
from typing import  Literal,Optional


class DeliveryBase(BaseModel):
    customer_phone:str=Field(...,pattern=r'^\+?\d{9,15}$',title="phone number",examples=["+254712345678","+254712345678"])
    customer_id:str=Field(...,pattern=r'^\d{7,11}$',title="id",examples=["123456789","1234567890"])
    customer_name:str=Field(...,min_length=2,max_length=100)
    customer_address: str = Field(..., min_length=2, max_length=100)
    delivery_type:str=Field(...,min_length=2,max_length=100)




class DeliveryCreate(DeliveryBase):
    pass



class DeliveryUpdate(BaseModel):
    status: Literal["delivered", "in-transit", "approve"] = Field(..., examples=["delivered", "in-transit", "approve"])



class DeliveryPostOutput(BaseModel):
    id: int
    customer_id: str
    delivery_type: str
    customer_phone: str
    customer_name: str
    customer_address: str
    manager_phone: str
    status: str


    class Config:
        from_attributes = True



class DeliveryGetOutput(BaseModel):
    id:int
    customer_id: str
    delivery_type: str
    customer_phone:str
    customer_name: str
    customer_address: str
    manager_phone:str
    status:str
    created_at: datetime
    predicted_eta_minutes: Optional[float] = None

    class Config:
        from_attributes = True



class DeliveryPutOutput(BaseModel):
    id:int
    delivery_type:str
    status:str
    created_at:datetime

    class Config:
        from_attributes = True

