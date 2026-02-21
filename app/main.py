from fastapi import FastAPI, Response, HTTPException, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from .database import engine, get_db
from . import utils
from .routers import post, users

load_dotenv()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

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

app.include_router(post.router)
app.include_router(users.router)

# @app -> is a decorator, to Connect function to API
# .get -> http method to get data to user
# ("/") -> what shld happen, when user opens base url
@app.get("/")
async def root():
    return {"message":"Hello World"}