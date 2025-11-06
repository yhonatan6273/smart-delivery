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
from datetime import datetime

#the user must be logged in to access these routes


router=APIRouter(prefix="/deliveries",tags=["deliveries"])


@router.get("", response_model=List[deliveries.DeliveryGetOutput])
#this function allow normal user to see all his deliveries.
#the function will allow admin user to see all the deliveries from all the users in the database.
def get_deliveries(db: Session= Depends(get_db),current_user: users.TokenData = Depends(oauth2.get_current_user)):
    
    if current_user.role == "admin":
        deliveries_query = db.query(models.Delivery).all()
    else:
        deliveries_query = db.query(models.Delivery).filter(models.Delivery.user_id == current_user.id).all()
    return deliveries_query






@router.post("", status_code=status.HTTP_201_CREATED,response_model=deliveries.DeliveryPostOutput)
#this function allow user to creates a new delivery and save it in the database
def make_delivery(
    delivery: deliveries.DeliveryCreate, db: Session= Depends(get_db),
    current_user: users.TokenData = Depends(oauth2.get_current_user)
    ):
    #default manager phone and status for new delivery    
    phone="053-9236230"
    make_status="approve"

    #validate the address using Google Maps API
    if not validate_address(delivery.customer_address):
        raise HTTPException(status_code=400, detail="the address is not valid according to Google Maps")

    #create new delivery
    new_delivery=models.Delivery(**delivery.model_dump(),manager_phone=phone,status=make_status,user_id=current_user.id)
    #add the new delivery to the database
    db.add(new_delivery)
    #commit the changes
    db.commit()
    #refresh the instance to get the new id
    db.refresh(new_delivery)
    #creating all the data from the new delivery to send to Kafka
    delivery_data = {
        "id": new_delivery.id,
        "user_id": new_delivery.user_id,
        "customer_name": new_delivery.customer_name,
        "customer_phone": new_delivery.customer_phone,
        "customer_id": new_delivery.customer_id,
        "origin_address": "Tel Aviv",
        "destination_address": new_delivery.customer_address,
        "delivery_type": new_delivery.delivery_type,
        "status": new_delivery.status
    }
    now = datetime.now()
    hour = now.hour
    day_of_week = now.weekday()
    #add hour_of_day and day_of_week to the preparation data to send to Kafka
    delivery_data["hour_of_day"] = hour
    delivery_data["day_of_week"] = day_of_week
    #we send all the new delivery data to Kafka using the send_delivery_report_avro function
    send_delivery_report_avro(delivery_data)
    #we can now return the new delivery with all its details to the user
    return new_delivery




@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
#this function allow normal user to delete display by by him 
#admin user can delete any delivery from any users
def delete_delivery(id:int,db: Session= Depends(get_db),
                     current_user: users.TokenData = Depends(oauth2.get_current_user)):

    delivery_query = db.query(models.Delivery).filter(models.Delivery.id == id)
    delivery_to_delete = delivery_query.first()
         
    if delivery_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Delivery with id: {id} not found")
    
    #only the user who created the delivery or an admin can delete it
    if delivery_to_delete.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
   
    delivery_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)






@router.put("/{id}", response_model=deliveries.DeliveryPutOutput)
def update_delivery(id:int, delivery: deliveries.DeliveryUpdate, db: Session= Depends(get_db),
                    current_user: users.TokenData = Depends(oauth2.get_current_user)):

    delivery_query=db.query(models.Delivery).filter(models.Delivery.id==id)
    existing_delivery = delivery_query.first()
    
    
    if existing_delivery is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Delivery with id: {id} not found")

    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
        
    if existing_delivery.status==delivery.status and current_user.role == "admin":
        if delivery.status=='approve':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didnt changed, you can change only to status 'delivered' or 'in-transit'")
        elif delivery.status=='in-transit':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didnt changed, you can change only to status 'delivered' or 'approve'")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didnt changed, you can change only to status 'in-transit' or 'approve'")
    
        

    delivery_query.update(delivery.model_dump(),synchronize_session=False)
    db.commit()
    
    db.refresh(existing_delivery)
    delivery_data = {
        "id": existing_delivery.id,
        "user_id": existing_delivery.user_id,
        "customer_name": existing_delivery.customer_name,
        "customer_phone": existing_delivery.customer_phone,
        "customer_id": existing_delivery.customer_id,
        "origin_address": "Tel Aviv", 
        "destination_address": existing_delivery.customer_address,
        "delivery_type": existing_delivery.delivery_type,
        "status": existing_delivery.status,
        "hour_of_day": datetime.now().hour,
        "day_of_week": datetime.now().weekday()
    }

    
    send_delivery_report_avro(delivery_data)
    
    return existing_delivery



@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=deliveries.DeliveryGetOutput)

def get_prediction(id:int,db: Session= Depends(get_db),
                     current_user: users.TokenData = Depends(oauth2.get_current_user)):
    delivery = db.query(models.Delivery).filter(models.Delivery.id == id).first()

    #check if  delivery exists
    if not delivery:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Delivery with id: {id} not found")
    
    #check for permissions
    if delivery.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to view this delivery")
    
    # If everything is okay, return the delivery
    return delivery