from fastapi import FastAPI
from .database import engine
from .routers import post, users, auth, votes
from . import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

# @app -> is a decorator, to Connect function to API
# .get -> http method to get data to user
# ("/") -> what shld happen, when user opens base url
@app.get("/")
async def root():
    return {"message":"Hello World"}