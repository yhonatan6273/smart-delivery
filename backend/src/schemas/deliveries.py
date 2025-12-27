from datetime import datetime
from pydantic import BaseModel,Field, field_validator
from typing import  Literal,Optional
from src.utils.google_map import validate_address

#this schema is the base for crating and updating deliveries
class DeliveryBase(BaseModel):
    customer_phone:str=Field(...,pattern=r'^\+?\d{9,15}$',title="phone number",examples=["+254712345678","+254712345678"])
    customer_id:str=Field(...,pattern=r'^\d{7,11}$',title="id",examples=["123456789","1234567890"])
    customer_name:str=Field(...,min_length=2,max_length=100)
    customer_address: str = Field(..., min_length=2, max_length=100)
    delivery_type:str=Field(...,min_length=2,max_length=100)


    #validate address using google maps api
    @field_validator('customer_address')
    @classmethod
    def check_address_with_google(cls, v):
        
            valid_address = validate_address(v)
            
            
            if not valid_address:
                raise ValueError("Address not valid according to Google Maps")
            
            return valid_address



#we take all fields from DeliveryBase for creating a delivery
class DeliveryCreate(DeliveryBase):
    pass


#this schema is for output after creating a delivery
class DeliveryPostOutput(BaseModel):
    id: int
    customer_id: str
    delivery_type: str
    customer_phone: str
    customer_name: str
    customer_address: str
    manager_phone: str
    status: str

    #turn sqlalchemy object to pydantic model
    class Config:
        from_attributes = True





#this schema is for output when getting deliveries
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
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


#we take only status field for updating a delivery
class DeliveryUpdate(BaseModel):
    status: Literal["delivered", "in-transit", "approve"] = Field(..., examples=["delivered", "in-transit", "approve"])



#this schema is for output when updating a delivery
class DeliveryPutOutput(BaseModel):
    id:int
    delivery_type:str
    status:str
    created_at:datetime

    class Config:
        from_attributes = True

