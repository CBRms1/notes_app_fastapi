from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from dependencies import get_session
from security import hash_password
from schemas import UserSchema

auth_router = APIRouter(prefix="/auth", tags={"AUTH"})

@auth_router.get("/")
async def root():
    return {"message": "auth root"}

@auth_router.post("/create")
async def create(user_schema: UserSchema, session=Depends(get_session)):
    user_exists = session.query(User).filter(User.email==user_schema.email).first()

    if user_exists:
        raise HTTPException(status_code=400, detail="user with this email already exists")

    hashed = hash_password(user_schema.password)

    new_user = User(
        name=user_schema.name, 
        email=user_schema.email, 
        password=hashed
    )

    session.add(new_user)
    session.commit()

    return {"message": f"user {new_user.name} with email {new_user.email} created!"}