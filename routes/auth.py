from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
import models
from starlette import status
from utils import Hasher, TokenMethods
from settings import settings
import schemas


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

with open(r"keys/private.pem") as f:
    PRIVATE_KEY = f.read()

with open(r"keys/public.pem") as f:
    PUBLIC_KEY = f.read()

def get_current_user(db:Annotated[Session,Depends(get_db)], token:Annotated[str,Depends(oauth2_scheme)]):
    token_data = TokenMethods.verify_token(token=token,
                                           secret_key=PUBLIC_KEY,
                                           algorithm=settings.ALGORITHM)
    user = db.query(models.User).filter_by(email=token_data.email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/token",response_model=schemas.Token)
async def login(db:Annotated[Session,Depends(get_db)],form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_user = db.query(models.User).filter_by(email=form_data.username).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password") 
    
    if not Hasher.verify_password(plain_password=form_data.password,hashed_password=db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"})
    
    payload = {"sub":db_user.email}
    access_token_expires = timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenMethods.create_token(data=payload,
                                            expires_delta=access_token_expires,
                                            secret_key=PRIVATE_KEY,
                                            algorithm=settings.ALGORITHM)
    
    return schemas.Token(access_token=access_token)
    