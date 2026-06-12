from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i, post
        

@app.delete("/posts/{id}")
def delete_post(id: int):
    i, post = find_post(id)

    if not post: #or if i == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    my_posts.pop(i) #to remove the post from the my_posts list

    return Response(status_code=status.HTTP_204_NO_CONTENT) #to return a response with status code 204, which means no content, since we are deleting the post and not returning anything