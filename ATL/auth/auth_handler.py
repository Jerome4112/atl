from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Union
from datetime import timedelta, datetime
from fastapi import HTTPException, status



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

SECRET_KEY = "58381ae4f261e012b04af109cc4a8e36468345bd243fdfed49d349f1c59dca4d3921a6aed04eeee48a3732b24cd63909ff0585a6dc6924c3cfa37e9845ac6c17"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Union [timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})
    #Create Access Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def is_token_valid(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire = payload.get("exp")
        if expire:
            if expire < datetime.timestamp(datetime.utcnow()):
                return False
            else:
                return True
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token ist not valid",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
