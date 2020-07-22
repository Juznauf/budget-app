"""
will use this to call the main application as well as to set the global configurations for our application
"""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/blog")
async def blog():
    return {"thisblog": "Hello blog"}
