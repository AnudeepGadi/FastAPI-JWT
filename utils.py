from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt
from passlib.context import CryptContext
import schemas
from starlette import status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password:str, hashed_password:str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)


class TokenMethods():
    @staticmethod
    def create_token(data:dict, expires_delta:timedelta, secret_key:str, algorithm:str) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp":expire})
        encoded_jwt = jwt.encode(payload=to_encode, key=secret_key, algorithm=algorithm)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token:str, secret_key:str, algorithm:str) -> schemas.TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, secret_key, algorithms=[algorithm])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = schemas.TokenData(email=email)
            return token_data
        except jwt.InvalidTokenError:
            raise credentials_exception
