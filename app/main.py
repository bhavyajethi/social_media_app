from fastapi import FastAPI, Response, HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

app = FastAPI()
load_dotenv()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

USER = os.getenv('user')
PASSWORD = os.getenv('password')
HOST = os.getenv('host')
# print(f"DEBUG HOST: '{HOST}'")
PORT = os.getenv('port')
DBNAME = os.getenv('dbname')

try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        cursor_factory=RealDictCursor,
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    # cursor.execute("SELECT NOW();")
    # result = cursor.fetchone()
    # print("Current Time:", result)

    # Close the cursor and connection
    # cursor.close()
    # connection.close()
    # print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
    time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, 
{"title": "favourite food", "content": "I love pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

# @app -> is a decorator, to Connect function to API
# .get -> http method to get data to user
# ("/") -> what shld happen, when user opens base url
@app.get("/")
async def root():
    return {"message":"Hello World"}

# order of the request matters, as the top one gets executed
@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"data":new_post}

# consider title as str, content as str for schema

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
   
    deleted_post = cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    cursor.fetchone()
    connection.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    # no need to send data or message back while deleting a post, just send status code
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return {"data":updated_post}