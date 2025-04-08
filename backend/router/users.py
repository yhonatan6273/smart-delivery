from fastapi import HTTPException
from fastapi import FastAPI, Response, status,Depends,APIRouter
from typing import List



from backend.db.database import get_db
from backend.Models import models
from sqlalchemy.orm import Session
from backend import schemas
from backend.utils import pwt_context



router=APIRouter(prefix="/users",tags=["users"])


@router.get("/{id}",response_model=schemas.UserOutput)
def get_user(id:int,db:Session= Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    if user_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} does not exist')
    return user_query



#creat users
@router.post("",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOutput)
def make_user(user:schemas.UserCreate,db: Session= Depends(get_db)):
    # hash the password for better security
    hashed_password = pwt_context.hash(user.password)
    user.password = hashed_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh( new_user)
    return new_user


