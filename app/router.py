"""
This file should include logic for the users as well as the items

Should handle the response to the clients

Router imports from budget to access the user functions

To keep things organize, the path operations related to our user is seperated from main.

"""
from typing import Optional 

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from budget import User, Budget, db

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(collection, username: str):
    """
    returns our collections object
    for this instance the token is the same
    as the username
    """
    return collection.find_one({"_id": username})

def decode_token(token):
    """
    no decoding used for now as user has no password set
    """
    return User(user_id = token) #set the decoding here

def get_current_user(token:str = Depends(oauth2_scheme)):
    user = get_user(db.banks_users, token)
    return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    if get_user(db.banks_users, username) is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = get_user(db.banks_users, username)
    return {"access_token": user['_id'], "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    will show the users transactions located in the "banks_users" 
    collection 
    """
    return current_user

@router.post("/users/me/create_budgets")
async def users_create_budget(
                            pb_identifier=Form(...),
                            category=Form(...),
                            amount=Form(...),
                            budget_type=Form(...),
                            current_user: User = Depends(get_current_user), 
                            ):
    """
    form for creating a new budget

    alternatively can use default param current user instead
    of using the pb_identifier
    """

    try:
        new_budget = Budget(
            pb_identifier=pb_identifier,
            category=category,
            amount=amount,
            budget_type=budget_type)
        new_budget.create_budget()
        result_msg = {"status": "success", 
        "message": "successfully created budget"}
    except:
        # errors include validation errors as well as db errors 
        # check budget file
        result_msg = {"status": "error", 
        "message": "failed to create budget"}
    

    return result_msg


@router.get("/users/me/budgets")
async def read_budgets(
                    current_user: User = Depends(get_current_user), 
                    ):
    """
    shows all the valid budgets
    """
    all_budgets = db.budget_users.find_one({'_id':current_user['_id']})
    
    return all_budgets
