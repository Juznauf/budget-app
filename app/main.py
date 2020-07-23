"""
will use this to call the main application as well as to set the global configurations for our application

will set the api calls for the index page

all the api calls to the user will be done in the router module
"""
from typing import List, Optional # for type hints

from fastapi import FastAPI, Query, status # status for post request hints
from pydantic import Basemodel 

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/blog")
async def blog():
    return {"thisblog": "Hello blog"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    """
    the {item_id} will be completed in the get request
    """
    return {"item_id": item_id}


