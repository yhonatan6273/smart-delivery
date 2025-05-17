from fastapi import HTTPException
from fastapi import status,Depends,APIRouter
from backend.db.database import get_db
from backend.models import models
from sqlalchemy.orm import Session
from backend.schemas import deliveries,users
from backend.utils.UtilsLogin import hash_password




router=APIRouter(prefix="/users",tags=["users"])




@router.get("/{id}", response_model=users.UserOutput)

def get_user(id:int,db:Session= Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id).first()
    
    if user_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} does not exist')
    
    return user_query



#creat users
@router.post("", status_code=status.HTTP_201_CREATED, response_model=users.UserOutput)

def create_user(user: users.UserCreate, db: Session= Depends(get_db)):
    # hash the password for better security
    hashed_password=hash_password(user.password)
    user.password = hashed_password
    
    new_user=models.User(email=user.email,password=hashed_password,role="user")
    
    if db.query(models.User).filter(models.User.email == new_user.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists try another")
    
    db.add(new_user)
    db.commit()
    db.refresh( new_user)
    return new_user


