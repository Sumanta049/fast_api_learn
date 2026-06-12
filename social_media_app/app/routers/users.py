from fastapi import APIRouter, FastAPI, Response, status, HTTPException, Depends
from sqlmodel import Session
from .. import models
from ..database import get_session
from ..schemas import CreateUser, UserResponse
from ..utils import hash


router = APIRouter(
    prefix="/users",
    tags=["users"] #for grouping in docs
)



# ============ users ============
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_session)):

    #hash the password before saving to database
    hashed_password = hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, session: Session = Depends(get_session)):
    user = session.get(models.Users, id)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {id} not found"
    )