from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
#this returns the username and password in the form data, we can use it to authenticate the user

from ..models import Users
from ..database import get_session
from ..schemas import userLogin, token
from ..utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    tags=["auth"] #for grouping in docs
) 


@router.post("/login", response_model=token)
# def login(curr_user: userLogin, session: Session = Depends(get_session)):
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

    #email check
    #db_user = session.exec(select(Users).where(Users.email == curr_user.email)).first()

    #but when using OAuth2PasswordRequestForm
    #email becomes username 
    db_user = session.exec(select(Users).where(Users.email == form_data.username)).first()

    #check if user exists
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    #check password
    if not verify(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid password"
        )
    
    #create token
    token = create_access_token(data = {"user_id": db_user.id})

    return {"access_token": token, "token_type": "bearer"}
