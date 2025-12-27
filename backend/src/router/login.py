from fastapi import HTTPException
from fastapi import status,Depends,APIRouter
from src.auth import oauth2
from fastapi.security import  OAuth2PasswordRequestForm
from src.db.database import get_db
from src.models import models
from sqlalchemy.orm import Session
from src.schemas import users
from src.utils import UtilsLogin

router=APIRouter(prefix="/login",tags=["login"])


#function for handle access for different accounts
#if the user given the correct password and email he will get a token to get in his account
@router.post("",response_model=users.Token)

def user_login(user_validation: OAuth2PasswordRequestForm=Depends(), db: Session= Depends(get_db)):

    user=db.query(models.User).filter(models.User.email==user_validation.username).first()
    
    if not user or  not UtilsLogin.verify_password(user_validation.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"the password or the email address is invalid")
    
    access_token= oauth2.create_access_token(data={"user_id":user.id, "role": user.role})

    return{"access_token":access_token,"token_type":"bearer"}

