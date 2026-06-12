#retreiving one singular post

from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]
class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value   
    rating: Optional[int] = None #optional value, can be null

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/posts/{id}") #path parameter-str (manually convert to int), it will be passed in the url
def get_post(id: int, response: Response):
    post = find_post(id)

    # if post:
    #     return {"post_detail": post} #usually status_code = 200, if found
    # response.status_code = status.HTTP_404_NOT_FOUND #to set the status code to 404 if post not found
    # return {"message": f"post with id {id} not found"}
    # #404 not found 

#another way to do it is to raise an HTTPException
    if post:
        return {"post_detail": post} #usually status_code = 200, if found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail=f"post with id {id} not found")

#anytime we create we must send 201, not 200
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id'] = len(my_posts) + 1 #to add id to the post dict
    my_posts.append(post_dict) 
    return {"new_post": post_dict}