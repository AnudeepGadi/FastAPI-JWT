from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME:str
    APP_SUMMARY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    
    class Config:
        env_file = ".env"


settings = Settings()