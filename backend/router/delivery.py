from fastapi import HTTPException
from fastapi import FastAPI, Response, status,Depends,APIRouter
from typing import List



from backend.db.database import get_db
from backend.Models import models
from sqlalchemy.orm import Session
from backend import schemas



router=APIRouter(prefix="/deliveries",tags=["deliveries"])





#geting all the deliveries in the data
@router.get("",response_model=List[schemas.DeliveryPostGetOutput])
def get_deliveries(db: Session= Depends(get_db)):
    deliveries=db.query(models.Delivery).all()
    return deliveries

#user creating new delivery we sending it to the data
@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.DeliveryPostGetOutput)
def make_delivery(delivery:schemas.DeliveryCreate,db: Session= Depends(get_db)):

    new_delivery=models.Delivery(**delivery.model_dump())
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
@router.put("/{id}",response_model=schemas.DeliveryPutOutput)
def update_delivery(id:int,delivery:schemas.DeliveryUpdate,db: Session= Depends(get_db)):

    delivery_query=db.query(models.Delivery).filter(models.Delivery.id==id)
    if delivery_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="delivery not found")
    if delivery_query.first().status==delivery.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="status not changed, you can change only status")

    delivery_query.update(delivery.model_dump(),synchronize_session=False)
    db.commit()
    return delivery_query.first()
