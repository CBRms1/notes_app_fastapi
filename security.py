# pass hash and create token

from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from jose import jwt
from config import ACCESS_TOKEN_EXPIRE_TIME, ALGORITHM, SECRET_KEY

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_token(user_id, token_type="access"):
    if token_type == "refresh":
        token_expire_time=ACCESS_TOKEN_EXPIRE_TIME*24
    else:
        token_expire_time=ACCESS_TOKEN_EXPIRE_TIME
    
    expiration_date = datetime.now(timezone.utc) + timedelta(hours=token_expire_time)

    dic_info = {"sub": str(user_id), "exp": expiration_date}

    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return encoded_jwt