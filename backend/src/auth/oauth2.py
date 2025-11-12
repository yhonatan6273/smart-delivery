from datetime import datetime, timedelta
from src.schemas import users
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.db.database import get_db
from src.models import models
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)  # Default to 30 minutes if not set

#function to create a token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



#function checks if the token that the user gave him is valid or not
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = users.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data

#function that gives the user his account for the database if the token is valid.
def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception= HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token=verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id==token.id).first()
    return user

