from typing import Optional

from pydantic import BaseModel, EmailStr, conint, Field
from typing_extensions import Annotated
from datetime import datetime




class UserBase(BaseModel):
    email: EmailStr

class CreateUser(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class userLogin(BaseModel):
    email: EmailStr
    password: str



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# Pydantic model for request validation
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

class PostResponse(PostBase):
    #inheritance
    user_id: int
    id: int
    created_at: datetime
    user: UserResponse 

    class Config:
        from_attributes = True #orm_mode = true

class PostOut(BaseModel):
    Post_new: PostResponse
    votes: int

    class Config:
        from_attributes = True
#with vote case 


class token(BaseModel):
    access_token: str
    token_type: str

class tokenData(BaseModel):
    id: Optional[int] = None




class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)] #conint(le=1) 
    #le means less than or equal to 1, so the value of dir can be either 0 or 1. 
    # 0 means downvote and 1 means upvote.