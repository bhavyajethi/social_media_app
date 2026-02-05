from fastapi import FastAPI

app = FastAPI()

# @app -> is a decorator, to Connect function to API
# .get -> http method to get data to user
# ("/") -> what shld happen, when user opens base url
@app.get("/")
async def root():
    return {"message":"Hello World"}

# order of the request matters, as the top one gets executed
@app.get("/posts")
async def get_posts():
    return {"data1":"This is the 1st post"}