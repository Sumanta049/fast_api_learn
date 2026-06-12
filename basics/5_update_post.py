from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #default value   
    rating: Optional[int] = None #optional value, can be null

def find_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i, post

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    i, post_to_update = find_post(id)
    print(post)

    if not post_to_update: #or if i == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    post_dict = post.model_dump() #to convert the post object to a dictionary
    post_dict['id'] = id #to add the id to the post dictionary

    my_posts[i] = post_dict #to update the post in the my_posts list

    return {"data": post_dict} #to return the updated post as a response



#for docs
#http://localhost:8000/docs

#fastapi automatically generates a doc for you
#you can also use http://localhost:8000/redoc for a different style of documentation