from fastapi import FastAPI
from database import engine
from database import Base
from routes.task import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)