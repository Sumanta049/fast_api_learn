# old implementation using jose-python for JWT handling
# from jose import jwt, JWTError

# new implementation using pyjwt
import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone
from .schemas import tokenData
from .database import get_session
from .models import Users
from .config import settings

from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer


# from auth.py file, login is the path where we will get the token from, 
# it is the endpoint where we will send the username and password to get the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#secret key
#algorithm
#expiration time

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# we can decode our jwt token by vising the website jwt.io and pasting the token there,
#  it will show us the payload and header of the token. 
# We can also verify the signature by pasting the secret key there. 
# If the signature is valid, it means that the token is not tampered with and is valid.

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = tokenData(id= id)
        return token_data
    
    except InvalidTokenError as e:
        raise credentials_exception
    


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return verify_access_token(token, credentials_exception)



def get_current_user(token: str = Depends(oauth2_scheme), get_db: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = get_db.exec(select(Users).where(Users.id == token_data.id)).first()

    if user is None:
        raise credentials_exception
    return user