"""
This file should include logic for the users as well as the items

Should handle the response to the clients

Router imports from budget to access the user functions

To keep things organize, the path operations related to our user is seperated from main.

"""

from fastapi import APIRouter, Form

router = APIRouter()


@router.post("/login/")
async def login(user_id : str = Form(...)): # we only require the user id to verify 

@router.get("/users/", tags=["users"])
def read_users():
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
