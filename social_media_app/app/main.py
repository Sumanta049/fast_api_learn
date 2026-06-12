"""
Consolidated FastAPI application combining all basics
Docs: https://fastapi.tiangolo.com/tutorial/first-steps/
"""

from fastapi import FastAPI
from sqlmodel import SQLModel

from .database import engine
from .routers import posts, users, auth, votes

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5432",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://www.google.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# SQLModel.metadata.create_all(engine)  # use alembic migrations instead


# ============ Documentation ============
# To run: uvicorn app.main:app --reload
# Swagger UI Docs: http://localhost:8000/docs
# ReDoc Docs: http://localhost:8000/redoc


# routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)
