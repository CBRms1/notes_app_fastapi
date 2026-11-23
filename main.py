from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

from auth_route import auth_router
from notes_route import notes_router

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/")
async def root():
    return {"message": "Hello world"}