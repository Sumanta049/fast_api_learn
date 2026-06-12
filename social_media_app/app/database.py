#using orm instead of raw sql queries
# sqlalchemy 
from time import time
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .config import settings


# Format: postgresql://user:password@host:port/database_name
#postgres_url = "postgresql://root:12345678@localhost:5432/FAST_API_LEARN"
postgres_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Create the engine (you no longer need connect_args)
engine = create_engine(postgres_url)

#for sql alchemy, base class is needed to create models
# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

#sqlalchemy session dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
def get_session():
    with Session(engine) as session:
        yield session


# =========== postgres connection to database =============
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            cursor_factory=RealDictCursor #gives col names
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Error connecting to database:", e)
        time.sleep(5)  # wait before retrying

