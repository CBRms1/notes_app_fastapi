from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from dependencies import get_session
from pwdlib import PasswordHash
from security import password_hash

auth_router = APIRouter(prefix="/auth", tags={"AUTH"})

@auth_router.get("/")
async def root():
    return {"message": "auth root"}

@auth_router.post("/create")
async def create(name:str, email: str, password: str, session=Depends(get_session)):
    user_exists = session.query(User).filter(User.email==email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="user with this email already exists")

    hashed = password_hash.hash(password)

    new_user = User(name=name, email=email, password=hashed)
    session.add(new_user)
    session.commit()
    return {"message": f"user {name} with email {email} created!"}