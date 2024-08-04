from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password:str = Field(min_length=8)
    is_active:bool = Field(default=True)

    @field_validator("password", mode="before")
    def validate_strength(cls, password:str):
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter.')
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValueError('Password must contain at least one lowercase letter.')
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one digit.')
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError('Password must contain at least one special character.')
        
        return password
    

class User(UserBase):
    id:int
    is_active:bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")

class TokenData(BaseModel):
    email:str