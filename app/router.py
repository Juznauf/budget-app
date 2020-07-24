"""
This file should include logic for the users as well as the items

Should handle the response to the clients

Router imports from budget to access the user functions

To keep things organize, the path operations related to our user is seperated from main.

"""
from typing import Optional 

from fastapi import APIRouter, Form, Depends
# from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

import budget
# from budget import User # import for validation 

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    """
    returns our collections object
    """
    return db.find_one({"_id": username})


def decode_token(token):
    """
    no decoding used for now as user has no password set
    """
    return budget.User(user_id = token) #set the decoding here

def get_current_user(token:str = Depends(oauth2_scheme)):
    user = get_user(budget.users_collection, token)
    return user




@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    if get_user(budget.users_collection, username) is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = get_user(budget.users_collection, username)
    return {"access_token": user['_id'], "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: budget.User = Depends(get_current_user)):
    return current_user



# @router.get("/user/")
# def 
# # @router.get("/users/", tags=["users"])
# # def read_users():
# #     return {"message": "Hello World"}


# @app.get("/blog")
# async def blog():
#     return {"thisblog": "Hello blog"}


# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     """
#     the {item_id} will be completed in the get request
#     """
#     return {"item_id": item_id}
