from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value   
    rating: Optional[int] = None #optional value, can be null
    
#it checks if those values exist in the request body and its type
#else throws error

@app.get("/posts")
def get_posts():
    return {"posts": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    print (new_post)
    print (new_post.dict()) #to convert to dict
    #dict is deprecated in favor of model_dump() in pydantic v2
    #new version: new_post.model_dump()

    post_dict = new_post.model_dump()
    post_dict['id'] = len(my_posts) + 1 #to add id to the post dict
    my_posts.append(post_dict) #to add the post dict to the my_posts list
    #return {"new_post": f"Post created with title {new_post.title} and content {new_post.content} and published status {new_post.published} and rating {new_post.rating}"}
    return {"new_post": post_dict}