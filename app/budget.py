"""
will include all the logic for creating the budgets

will have the path functions import from this file
"""

# logic here to create the budget document which will be written into the plannerbee database, under the "budgets_users" collection of the M0 cluster mongodb database.



# the request from the user is as such, a pb_identifier,category,amount, budget_type, the response to the client is as follows, we need to return if the budget has been successfully created or not in our database cluster. So we need to respond with a custom error message in JSON format. So the budget module has to take care of the writes to our DB as well as the response to the client. 

# so in this module we shall initialize the database as well as perform CRUD on our db.

from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from datetime import datetime

client = MongoClient(
   "mongodb+srv://nauf:XdxCOlhec7iYftKE@cluster0.ngmxl.mongodb.net/plannerbee?retryWrites=true&w=majority")
db = client['plannerbee'] # init db 
# print(db.list_collection_names())
# for k in db.__dict__:
#     print(k, ':', db.__dict__[k]) to see the attributes in db 
users_collection = db['banks_users'] # for the collections of all transactions 
budget_collection = db['budget_users'] # for the collection of all budgets created

class User(BaseModel):
    """
    class is used for validation at user login 
    """
    user_id: str

    @validator('user_id')
    def check_user(cls, v):
        """
        this is a class method, v is the attr of the instance

        when validing the user sign in from, check that this user 
        exists in our database
        """
        if users_collection.find_one({"_id": v}) is None:
            # collection method will either return the documents which contain id or None 
            raise ValueError(
                    "username not found, please provide a valid username"
                            )

print(users_collection.full_name) # check if connection is succesful




class Budget(BaseModel):
    """
    Create budget model for the users 
    """

    pass


