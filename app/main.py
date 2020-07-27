"""
will use this to call the main application as well as to set the global configurations for our application

will set the api calls for the index page

all the api calls to the user will be done in the router module
"""
from typing import List, Optional # for type hints
import router
from fastapi import FastAPI, Query, status # status for post request hints

app = FastAPI()

app.include_router(router.router)


@app.get("/")
async def root():
    return {"message": "Hello User, Please go to root/docs"}
