"""
will include all the logic for creating the budgets

will have the path functions import from this file
"""

from typing import Optional

from pydantic import BaseModel, ValidationError, validator
from pymongo import MongoClient
from bson.son import SON
from datetime import datetime, timedelta
from calendar import monthrange

import secrets

client = MongoClient(
   "mongodb+srv://new_user_1:e7VwW5qSO3Gz9YVe@cluster0.ngmxl.mongodb.net/plannerbee?retryWrites=true&w=majority")
db = client.plannerbee # init db 

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
        if db.banks_users.find_one({"_id": v}) is None:
            # collection method will either return the documents which contain id or None 
            raise ValueError(
                    "username not found, please provide a valid username"
                            )
        return v


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
        v = v.lower()
        if v not in ["transfers", "shopping", "education", "personal_care"]:
            raise ValueError(
                "Not a valid category ! These are the list of valid categories"\
                    ":[transfers, shopping, education, personal_care]"
                            )
        return v
    
    @validator('budget_type')
    def valid_budget_type(cls, v):
        """
        check that it is either "Monthly" or "Annual"
        """

        if v.lower().title() not in ["Monthly", "Annual"]:
            raise ValueError(
                            "Not a valid budget type, budget type is "\
                            "either Monthly or Annual"
                            )
        return v.lower().title()

    def create_budget(
                    self, db=db
                    ):
        """
        create budget according to user defined params,
        if creation successful, return the budget object, 
        else return none
        """
        
        _id = self.pb_identifier
        local_currency_code = "SGD"
        category = self.category
        _type = self.budget_type
        current_time = datetime.now()
        created_at = current_time.strftime(format="%Y-%m-%dT%H:%M:%SZ")
        period = current_time.strftime(format="%m%Y")
        current_year = current_time.strftime(format="%Y")
        current_month = current_time.strftime(format="%m")
        current_month_year = current_time.strftime(format="%b %Y")


        def _get_local_currency_period_spent(_id=_id, category=category, current_time=current_time, 
                                            _type=_type,db=db):
            """
            """
            query = db.banks_users.find_one({"_id":_id})
            transactions: list = [query['transactions'][x] for x in query['transactions']]
            if _type=="Annual":
                current_year = current_time.strftime(format="%Y")
                currency_spent = sum(x['local_currency_amount'] for x in transactions
                                    if x['transacted_at'].split('-')[0] == current_year)
                                    # take for the entire year as all budgets are forward looking,hence 
                                    # the date the budget is created will always be later than the transactions
            else:
                current_year_mth = current_time.strftime(format="%Y-m")
                currency_spent = sum(x['local_currency_amount'] for x in transactions
                                    if '-'.join(x['transacted_at'].split('-')[:2]) == current_year_mth)
            
            return currency_spent
        
        def _generate_key():
            key_len = [4,2,2,2,6] # hex will double this len
            results = '-'.join(secrets.token_hex(x) for x in key_len)
            return results

        
        local_currency_amount_allowed = self.amount
        local_currency_period_spent = _get_local_currency_period_spent() # need to query this amount
        local_currency_period_remaining = local_currency_amount_allowed\
             - local_currency_period_spent
        budget_advise = "SGD 0/day"
        budget_notes = "status_above_100"

        # set budget period, budget notes
        if _type == "Annual":
            budget_period = f"01 Jan {current_year} - 31 Dec {current_year}"
            if local_currency_period_remaining > 0:
                final = f"31-12-{current_year}"
                days_remaining = datetime.strptime(f"{final}", "%d-%m-%Y")\
                    - current_time
                budget_advise = "SGD {0:.2f}/day".format(
                    local_currency_period_remaining/int(days_remaining.days)
                    )
                budget_notes = "status_below_100"

        if _type == "Monthly":
            end_of_mth = monthrange(year=int(current_year), month=int(current_month))[1]
            budget_period = f"01 {current_month_year} - {end_of_mth} {current_month_year}"
            if local_currency_period_remaining > 0:
                days_remaining = int(end_of_mth) - int(current_time.day)
                budget_advise = "SGD {0:.2f}/day".format(
                    local_currency_period_remaining/days_remaining
                    )
                budget_notes = "status_below_100"
            
        key = _generate_key()

        budget = {
                "category": category,
                "type": _type,
                "period": period,
                "budget_advise": budget_advise,
                "budget_period": budget_period,
                "local_currency_amount_allowed": local_currency_amount_allowed,
                "local_currency_period_spent": local_currency_period_spent,
                "created_at": created_at,
                "budget_notes": budget_notes
                }

        # write to db

        if db.budget_users.find_one({"_id":_id}):
            # update existing document
            db.budget_users.update_one(
                filter={"_id":_id},
                update={"$set":{f"budgets.{key}":budget}}
            )
        else:
            fresh_budget = {
                "_id": _id,
                "local_currency_code": "SGD",
                "budgets": {
                    key: budget
                }
            }
            db.budget_users.insert_one(fresh_budget)





if __name__ == "__main__":
    # for testing db connection 
    budget1 = Budget(**{'pb_identifier': "16cecd11-2f83-4864-bf6b-f270f4be88cb",
    'category': "shopping",
    'amount': 1000,
    'budget_type': "Annual"})
    budget2 = Budget(**{'pb_identifier': "16cecd11-2f83-4864-bf6b-f270f4be88cb",
    'category': "shopping",
    'amount': 90,
    'budget_type': "Monthly"})
    budget1.create_budget()
    budget2.create_budget()

