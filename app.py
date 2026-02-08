from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, 
{"title": "favourite food", "content": "I love pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# @app -> is a decorator, to Connect function to API
# .get -> http method to get data to user
# ("/") -> what shld happen, when user opens base url
@app.get("/")
async def root():
    return {"message":"Hello World"}

# order of the request matters, as the top one gets executed
@app.get("/posts")
async def get_posts():
    return {"data":my_posts}

@app.post("/posts")
async def create_posts(post: Post):
    post_dict = dict(post)
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data":post_dict}

# consider title as str, content as str for schema

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=404, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"message":post}