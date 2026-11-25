# auth route

from fastapi import APIRouter, Depends, HTTPException
from models.models import User, db
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from security import hash_password, verify_password, create_token
from schemas import UserSchema, LoginSchema
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags={"AUTH"})

def authenticate(email, password, session):
    user = session.query(User).filter(User.email==email).first()

    if not user:
        return False
    elif not verify_password(password, user.password):
        return False

    return user

@auth_router.get("/")
async def root():
    return {"message": "auth root"}

@auth_router.post("/create")
async def create(user_schema: UserSchema, session: Session=Depends(get_session)):
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

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session=Depends(get_session)):
    user = authenticate(login_schema.email, login_schema.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="invalid credentials")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_type="refresh")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

# authorize tests
@auth_router.post("/login-form")
async def login(form_data: OAuth2PasswordRequestForm=Depends(), session: Session=Depends(get_session)):
    user = authenticate(form_data.username, form_data.password, session)

    if not user:
        raise HTTPException(status_code=400, detail="invalid credentials")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_type="refresh")
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(user: User=Depends(verify_token)):
    access_token = create_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }