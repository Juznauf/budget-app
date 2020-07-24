"""
will include all the logic for creating the budgets

will have the path functions import from this file
"""

from typing import Optional

from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from datetime import datetime, timedelta

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


class Budget(BaseModel):
    """
    Create budget model for the users 
    """
    pb_identifier: str
    category: str
    amount: float
    budget_type: str


    @validator('category')
    def valid_category(cls, v):
        """
        check that category is one of 
        ["transfers", "shopping", "education", "personal_care"]
        """
        if v not in ["transfers", "shopping", "education", "personal_care"]:
            raise ValueError(
                "Not a valid category ! These are the list of valid categories"\
                    ":[transfers, shopping, education, personal_care]"
                            )
    
    @validator('budget_type')
    def valid_budget_type(cls, v):
        """
        check that it is either "Monthly" or "Annual"
        """

        if v.lower().title() not in ["Monthly", "Annual"]:
            raise ValueError(
                            "Not a valid budget type, budget type is"\
                            "either Monthly or Annual"
                            )

    def create_budget(
                    self, users_collection = users_collection,
                    budget_collection = budget_collection
                    ):
        """
        create budget according to user defined params,
        if creation successful, return the budget object, 
        else return none
        """
        _id = self.pb_identifier
        created_at = datetime.now().strftime(format="%Y-%m-%dT%H:%M:%SZ")
        budget = {"_id":_id,
                "budgets":{"created_at":created_at}}
        budget_collection.insert_one(budget)
        






if users_collection and budget_collection: # check if connection is succesful
    print(f"Successfully connected to collections {users_collection}\
     and {budget_collection}")



if __name__ == "__main__":
    budget1 = Budget(**{'pb_identifier': "16cecd11-2f83-4864-bf6b-f270f4be88cb",
    'category': "shopping",
    'amount': 100,
    'budget_type': "Annual"})
    # for i in range(2):
    #     budget1.create_budget()
        
