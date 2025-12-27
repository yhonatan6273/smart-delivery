from fastapi import HTTPException
from fastapi import status,Depends,APIRouter
from src.db.database import get_db
from src.models import models
from sqlalchemy.orm import Session
from src.schemas import users
from src.utils.UtilsLogin import hash_password




router=APIRouter(prefix="/users",tags=["Register"])



#searching users by id
@router.get("/{id}", response_model=users.UserOutput)

def get_user(id:int,db:Session= Depends(get_db)):
    
    # get user by id
    user_query = db.query(models.User).filter(models.User.id == id).first()
    #if user does not exist raise 404 error and return message
    if user_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} does not exist')
    
    return user_query



#create users
@router.post("", status_code=status.HTTP_201_CREATED, response_model=users.UserOutput)

def create_user(user: users.UserCreate, db: Session= Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    # check if email already exists
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists try another")
    
    # hash the password for better security
    hashed_password=hash_password(user.password)
    user.password = hashed_password
    #create new user
    new_user=models.User(email=user.email,password=hashed_password,role="user")
    #add the new user to the database
    db.add(new_user)
    #commit the changes
    db.commit()
    #refresh the instance to get the new id
    db.refresh(new_user)
    return new_user


