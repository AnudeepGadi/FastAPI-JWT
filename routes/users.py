from fastapi import APIRouter, Depends, HTTPException, Path
from database import get_db
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
import models
import schemas
from typing import List
from utils import Hasher
from routes.auth import get_current_user

router = APIRouter(
     prefix="/users",
     tags=["users"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def read_users(db: Annotated[Session,Depends(get_db)]):
    users = db.query(models.User).all()
    return users

@router.put("/{user_id}",status_code=status.HTTP_200_OK, response_model=schemas.User)
def update_user(db:Annotated[Session,Depends(get_db)], new_user_details:schemas.User, user_id:int=Path(ge=1)):
    user = db.query(models.User).filter_by(id=user_id).first()
    if user:
        user.is_active=new_user_details.is_active
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
    return user

@router.delete("/{user_id}",status_code=status.HTTP_200_OK)
def delete_user(db:Annotated[Session,Depends(get_db)],user_id:int=Path(ge=1)):
    user = db.query(models.User).filter_by(id=user_id).first()
    db.update(user)
    db.commit()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.User)
def create_user(user:schemas.UserCreate, db: Annotated[Session,Depends(get_db)]):
    check_user = db.query(models.User).filter_by(email=user.email).first()
    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already exists")
    
    hashed_password = Hasher.get_password_hash(user.password)
    created_user = models.User(email=user.email, hashed_password=hashed_password, is_active=user.is_active) 
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user

@router.get("/me/", response_model=schemas.User)
async def get_current_user_details(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user
