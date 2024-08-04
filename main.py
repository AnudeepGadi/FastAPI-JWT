from fastapi import FastAPI
from database import engine
import models
from routes import users,auth
from settings import settings


models.Base.metadata.create_all(bind=engine)
app = FastAPI(
        title=settings.APP_NAME,
        summary=settings.APP_SUMMARY
    )
app.include_router(users.router)
app.include_router(auth.router)

