"""
Consolidated FastAPI application combining all basics
Docs: https://fastapi.tiangolo.com/tutorial/first-steps/
"""
#sql query
#sqlalchemy - ORM - sqlmodel - ORM
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
import time
from . import models
from .database import engine, get_session
from sqlmodel import SQLModel, Session, select
from .schemas import CreatePost, UpdatePost



app = FastAPI()
# models.Base.metadata.create_all(bind=engine) #create tables in database based on models-sqlalchemy
SQLModel.metadata.create_all(engine)





# =========== postgres connection to database =============
import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="FAST_API_LEARN",
            user="root",
            password="12345678",
            cursor_factory=RealDictCursor #gives col names
        )
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Error connecting to database:", e)
        time.sleep(5)  # wait before retrying


# ============ get ============
# # GET root endpoint
# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     return {"posts": posts}

#orm - sqlmodel
@app.get("/sqlmodel")
def get_posts_sqlmodel(session: Session = Depends(get_session)):
    posts = session.exec(select(models.Post_new)).all() #returns sql query
    return {"posts": posts}

# ============ post ============
# POST posts with schema validation
@app.post("/posts")
def create_posts(new_post: CreatePost, status_code=status.HTTP_201_CREATED, db: Session = Depends(get_session)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (new_post.title, new_post.content, new_post.published)
    # )
    # created_post = cursor.fetchone()
    # conn.commit() #need to commit to save changes to database
    # return {"new_post": created_post}

    #orm - sqlmodel
    post = models.Post_new(
        title=new_post.title,
        content=new_post.content,
        published=new_post.published
    )
    #but this is inefficient for a lot of columns/info
    #so we do:
    #post_dict = new_post.dict()            #convert pydantic model to dict
    #post = models.Post_new(**post_dict)    #unpack dict to create sqlmodel
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"new_post": post}



# ============ id ============
# GET single post by id
@app.get("/posts/{id}")
def get_post(id: int, session: Session = Depends(get_session)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # # we need extra comma in (str(id),) to make it a tuple, 
    # # otherwise it will be treated as a string and cause an error
    # post = cursor.fetchone() 

    #orm - sqlmodel
    post = session.get(models.Post_new, id)

    if post:
        return {"post_detail": post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found"
    )


# ============ delete_post ============
@app.delete("/posts/{id}")
def delete_post(id: int, session: Session = Depends(get_session)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = session.get(models.Post_new, id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    session.delete(deleted_post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============ update_post ============
@app.put("/posts/{id}")
def update_post(id: int, post: UpdatePost, session: Session = Depends(get_session)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #     (post.title, post.content, post.published, str(id))
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = session.get(models.Post_new, id)

    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    
    updated_post.title = post.title
    updated_post.content = post.content
    updated_post.published = post.published
    session.add(updated_post)
    session.commit()
    session.refresh(updated_post)
    #for manually updating fields, we can also do:
    #updated_post.title = "new title", etc. but for a lot of fields, we can do:
    #post_data = post.dict() #convert pydantic model to dict
    #for key, value in post_data.items():
    #    setattr(updated_post, key, value) #set attribute of updated_post to value
    return {"data": updated_post}


# ============ Documentation ============
# To run: uvicorn app.main:app --reload
# Swagger UI Docs: http://localhost:8000/docs
# ReDoc Docs: http://localhost:8000/redoc
