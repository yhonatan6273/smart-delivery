from fastapi import HTTPException
from fastapi import Response, status,Depends,APIRouter
from typing import List
from backend.auth import oauth2
from backend.db.database import get_db
from backend.models import models
from sqlalchemy.orm import Session
from backend.schemas import deliveries,users

router=APIRouter(prefix="/deliveries",tags=["deliveries"])





#geting all the deliveries in the user database or in admin database
@router.get("", response_model=List[deliveries.DeliveryGetOutput])
def get_deliveries(db: Session= Depends(get_db), current_user: users.TokenData = Depends(oauth2.get_current_user)):
    if current_user.role == "admin":
        deliveries_query = db.query(models.Delivery).all()
    else:
        deliveries_query = db.query(models.Delivery).filter(models.Delivery.user_id == current_user.id).all()
    return deliveries_query

#user creating new delivery
#only after he logged to his user
@router.post("", status_code=status.HTTP_201_CREATED, response_model=deliveries.DeliveryPostOutput)
def make_delivery(delivery: deliveries.DeliveryCreate, db: Session= Depends(get_db),
                  current_user: users.TokenData = Depends(oauth2.get_current_user)):

    new_delivery=models.Delivery(**delivery.model_dump(),user_id=current_user.id)
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status not changed, you can change only status")

    delivery_query.update(delivery.model_dump(),synchronize_session=False)
    db.commit()
    return delivery_query.first()
