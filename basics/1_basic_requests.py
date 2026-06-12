#docs: https://fastapi.tiangolo.com/tutorial/first-steps/
from fastapi import FastAPI
from fastapi import Body

app = FastAPI()
    
#uvicorn basic_requests:app --reload in terminal to run the server


#app -> decorator
#get -> method
#"/" -> path
#root -> function name
#https methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Methods
@app.get("/")
def root(): #or async def root():
    return {"message": "Hello World ninjas"}

@app.get("/posts")
def read_posts():
    return {"message": "Reading posts"}

#for same url/path, the first mention wins
#that is: if we change read_posts path to "/", but keep it below root
#then it will return "hello world" instead of "reading posts"


#post req
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print (payload)
    return {"new_post": f"Post created with title {payload['title']} and content {payload['content']}"}
