from fastapi import HTTPException
from fastapi import Response, status,Depends,APIRouter
from typing import List
from src.auth import oauth2
from src.db.database import get_db
from src.models import models
from sqlalchemy.orm import Session
from src.schemas import deliveries
from src.utils.google_map import validate_address,get_directions, get_lat_long
from src.kafka.producer import send_delivery_request
from datetime import datetime



router=APIRouter(prefix="/deliveries",tags=["deliveries"])


@router.get("", response_model=List[deliveries.DeliveryGetOutput])
#this function allow normal user to see all his deliveries details including the predicted ETA minutes.
#the function will allow admin user to see all the deliveries from all the users in the database.
def get_deliveries(db: Session= Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    
    if current_user.role == "admin":
        deliveries_query = db.query(models.Delivery).all()
    else:
        deliveries_query = db.query(models.Delivery).filter(models.Delivery.user_id == current_user.id).all()
    return deliveries_query






@router.post("", status_code=status.HTTP_201_CREATED,response_model=deliveries.DeliveryPostOutput)
#this function allow user to creates a new delivery and save it in the database
def make_delivery(
    delivery: deliveries.DeliveryCreate,
    db: Session= Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
    ):
    
    #default manager phone and status for new delivery    
    phone="053-9236230"
    make_status="approve"
    lat, lng = get_lat_long(delivery.customer_address)

    #create new delivery
    new_delivery=models.Delivery(**delivery.model_dump(),manager_phone=phone,
                                 status=make_status,
                                 user_id=current_user.id,
                                 latitude=lat,
                                 longitude=lng)
                                    
        
    #add the new delivery to the database
    db.add(new_delivery)
    #commit the changes
    db.commit()
    #refresh the instance to get the new id
    db.refresh(new_delivery)
    #creating all the data from the new delivery to send to Kafka
    
    now = datetime.now()
    #this will be the payload to send to kafka topic (the values according to the value_schema in producer.py)
    kafka_payload = {
        "id": new_delivery.id,
        "destination_address": new_delivery.customer_address,
        "origin_address": "tel aviv dizengoff center", 
        "hour_of_day": now.hour,
        "day_of_week": now.weekday()
    }

    #send the delivery request to kafka topic
    send_delivery_request(kafka_payload)
    
    return new_delivery





@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
#this function allow normal user to delete display by by him 
#admin user can delete any delivery from any users
def delete_delivery(id:int, db: Session= Depends(get_db),
                     current_user: models.User = Depends(oauth2.get_current_user)):

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
def update_delivery(
    id:int,
    delivery: deliveries.DeliveryUpdate,
    db: Session= Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
    ):


    delivery_query=db.query(models.Delivery).filter(models.Delivery.id==id)
    delivery_to_update = delivery_query.first()
    
    
    if delivery_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Delivery with id: {id} not found")

    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
        
    if delivery_to_update.status==delivery.status and current_user.role == "admin":
        if delivery.status=='approve':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didn't changed, you can change only to status 'delivered' or 'in-transit'")
        elif delivery.status=='in-transit':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didn't changed, you can change only to status 'delivered' or 'approve'")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status didn't changed, you can change only to status 'in-transit' or 'approve'")
    
    delivery_query.update(delivery.model_dump(),synchronize_session=False)
    db.commit()
    
    db.refresh(delivery_to_update)
    return delivery_to_update
