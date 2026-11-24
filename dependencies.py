# dependencies used with Depends()

from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer

# oauth2 schema to authenticate with fastapi docs
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verify_token(token: str=Depends(oauth2_schema), session: Session=Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access danied")

    user = session.query(User).filter(User.id==user_id).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Access danied")
    
    return user

