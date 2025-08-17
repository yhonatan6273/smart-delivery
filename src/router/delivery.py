from fastapi import HTTPException
from fastapi import Response, status,Depends,APIRouter
from typing import List
from src.auth import oauth2
from src.db.database import get_db
from src.models import models
from sqlalchemy.orm import Session
from src.schemas import deliveries,users
from src.utils.google_map import validate_address
from src.kafka.producer import send_delivery_report_avro


router=APIRouter(prefix="/deliveries",tags=["deliveries"])




#geting all the deliveries in the user database or in admin database
@router.get("", response_model=List[deliveries.DeliveryGetOutput])

def get_deliveries(db: Session= Depends(get_db),current_user: users.TokenData = Depends(oauth2.get_current_user)):
    
    if current_user.role == "admin":
        deliveries_query = db.query(models.Delivery).all()
    else:
        deliveries_query = db.query(models.Delivery).filter(models.Delivery.user_id == current_user.id).all()
    return deliveries_query





#user creating new delivery
#only after he logged to his user
@router.post("", status_code=status.HTTP_201_CREATED,response_model=deliveries.DeliveryPostOutput)

def make_delivery(
    delivery: deliveries.DeliveryCreate, db: Session= Depends(get_db),
    current_user: users.TokenData = Depends(oauth2.get_current_user)
    ):

    if not validate_address(delivery.customer_address):
        raise HTTPException(status_code=400, detail="the address is not valid according to Google Maps")
    
    phone="053-9236230"
    make_status="approve"
    new_delivery=models.Delivery(**delivery.model_dump(),manager_phone=phone,status=make_status,user_id=current_user.id)
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    # Prepare the data to send to Kafka
    delivery_data = {
        "id": new_delivery.id,
        "user_id": current_user.id,
        "customer_name": new_delivery.customer_name,
        "customer_phone": new_delivery.customer_phone,
        "customer_id": new_delivery.customer_id,
        "origin_address": "Tel Aviv",
        "destination_address": new_delivery.customer_address,
        "delivery_type": new_delivery.delivery_type,
        "status": new_delivery.status
    }
    # Add customer details to the delivery data
    send_delivery_report_avro(delivery_data)

    return new_delivery






#chosing delivery id we want to delete and then deleting the orders from our data
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_delivery(id:int,db: Session= Depends(get_db)):
    
    delivery_query=db.query(models.Delivery).filter(models.Delivery.id==id)
    
    if delivery_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="delivery not found")
    
    delivery_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




#updating delivery in our data
@router.put("/{id}", response_model=deliveries.DeliveryPutOutput)

def update_delivery(id:int, delivery: deliveries.DeliveryUpdate, db: Session= Depends(get_db)):

    delivery_query=db.query(models.Delivery).filter(models.Delivery.id==id)
    
    if delivery_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="delivery not found")
    
    if delivery_query.first().status==delivery.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didnt changed, you can change only status")

    delivery_query.update(delivery.model_dump(),synchronize_session=False)
    db.commit()
    return delivery_query.first()
