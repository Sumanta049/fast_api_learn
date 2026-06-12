import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import SQLModel, Session, select
from sqlalchemy import func

from ..oauth2 import get_current_user
from .. import models
from ..database import engine, get_session
from ..schemas import CreatePost, PostOut, UpdatePost, PostResponse, CreateUser, UserResponse
from ..utils import hash
from typing import List, Optional



router = APIRouter(
    prefix="/posts",
    tags=["posts"] #for grouping in docs
)



# ============ get ============
# # GET root endpoint
@router.get("/", response_model=List[PostOut])
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     return posts
def get_posts(session: Session = Depends(get_session), 
              current_user: int = Depends(get_current_user),
              limit_post : int = 10,
              skip_post: int = 0,
              search: Optional[str] = ""):
    print(limit_post)
    #{{URL}}posts?limit_post=2&skip_post=2&search=keyword%20secondword in postman

    #posts = session.exec(select(models.Post_new).filter(models.Post_new.title.contains(search)).limit(limit_post).offset(skip_post)).all()

    #limit the number of posts returned to 10, we can also do offset for pagination
    #skip the first 10 posts and return the next 10 posts, etc. for pagination
    #search for posts with title containing the search string
    # %20 means space

    #posts = session.exec(select(models.Post_new)).all()


    post_votes = session.exec(
    select(models.Post_new, func.count(models.Vote.post_id).label("votes"))
    .join(models.Vote, models.Vote.post_id == models.Post_new.id, isouter=True)
    .group_by(models.Post_new.id)
    .filter(models.Post_new.title.contains(search))
    .limit(limit_post)
    .offset(skip_post)
    ).all()

    #for getting only the post of the user thats logged in
    #posts = session.exec(select(models.Post_new).where(models.Post_new.user_id == current_user.id)).all()
    

    return post_votes
    
    #return posts



# ============ post ============
# POST posts with schema validation
#we would want users to be logged in to create posts, 
# so we will use the get_current_user function from oauth2.py to get the current user 
# and check if they are logged in before allowing them to create a post.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(new_post: CreatePost, 
                 db: Session = Depends(get_session), 
                 current_user: int = Depends(get_current_user)):
    # cursor.execute(
    #     "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #     (new_post.title, new_post.content, new_post.published)
    # )
    # created_post = cursor.fetchone()
    # conn.commit() #need to commit to save changes to database
    # return {"new_post": created_post}


    print(current_user.email)
    #orm - sqlmodel
    # post = models.Post_new(
    #     title=new_post.title,
    #     content=new_post.content,
    #     published=new_post.published
    # )
    #but this is inefficient for a lot of columns/info
    #so we do:
    post = models.Post_new(**new_post.model_dump(), user_id=current_user.id)    #unpack dict to create sqlmodel
    db.add(post)
    db.commit()
    db.refresh(post)
    return post



# ============ id ============
# GET single post by id
@router.get("/{id}", response_model=PostOut)
def get_post(id: int, session: Session = Depends(get_session), current_user: int = Depends(get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    # # we need extra comma in (str(id),) to make it a tuple, 
    # # otherwise it will be treated as a string and cause an error
    # post = cursor.fetchone() 

    #orm - sqlmodel
    #post = session.get(models.Post_new, id)

    post = session.exec(
        select(models.Post_new, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post_new.id, isouter=True)
        .where(models.Post_new.id == id)
        .group_by(models.Post_new.id)
    ).first()

    # if post and post.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to view this post"
    #     )

    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} not found"
    )


# ============ delete_post ============
@router.delete("/{id}", response_model=PostResponse)
def delete_post(id: int, session: Session = Depends(get_session), current_user: int = Depends(get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = session.get(models.Post_new, id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )
    
    if deleted_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )
    

    session.delete(deleted_post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ============ update_post ============
@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: UpdatePost, session: Session = Depends(get_session), current_user: int = Depends(get_current_user)):
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
    if updated_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
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
    return updated_post
