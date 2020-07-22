One of the feature that we are providing to our users is the ability
to add budgets to keep track of their spending.

Your task is to create one REST API that can be used to create new budgets for our users.

The requirements for the API and the information you need are provided below.

### GENERAL REQUIREMENTS
____________________
1. You will be required to use FastAPI webframework and Mongodb

- FastAPI documentation can be found here: https://fastapi.tiangolo.com/ 
- You will need to set up a Mongodb Atlas free tier M0 cluster. The cluster will be used to store the user's budget and transaction information (more information below). You should be able to create the cluster after you set up an account at https://www.mongodb.com/cloud/atlas

2. Your API should follow the REST API guidelines.


### REQUIRED FILES
______________
1. **main.py**
2. **router.py**

You may refer to the FastAPI documentation [here](https://fastapi.tiangolo.com/tutorial/bigger-applications/) to look at examples of **main.py** and **router.py**


3. **budget.py**: contains the functions/logic that you need to create budgets.
4. **requirements.txt**: packages that need to be installed to set up the virtual environment to run the API


### API Requirements
________________
1. For this exercise, a user of your API should be able to send a request with the following fields to create a budget:

```
"pb_identifier": "16cecd11-2f83-4864-bf6b-f270f4be88cb"
"category": "dining"
"amount": 100
"budget_type": "Annual"
```

- `pb_identifier`: The unique identifier of the user that we are creating a budget for

- `category`: The transaction category that the user is creating the budget for.
In this scenario the user is creating a budget for the "dining" category. As such, only expenses (transactions with negative amounts) that are categorised as "dining" will be considered.
For simplicity, there are only four types of categories that the user can create a budget for: "transfers", "shopping", "education", "personal_care".

- `amount`: The maximum amount that the user can spend for the transaction category

- `budget_type`: There are only two options "Monthly" or "Annual". If "Monthly" is given, only
expenses for the month will be considered. If "Annual" is chosen, expenses for the whole
calendar year will be considered. For example, if a user creates a "Monthly" budget on 5th Jul 2020, only the expenses for 1st Jul - 5th Jul 2020 will be considered. Alternatively, if the user creates a "Annual" budget, the expenses for 1st Jan - 5th Jul 2020 will be considered.

2. For a budget to be considered successfully created, a document needs to be created in a "plannerbee" database, under the "budgets_users" collection of the M0 cluster mongodb database. An example schema of the document is shown below:

```
{
    "_id": "16cecd11-2f83-4864-bf6b-f270f4be88cb",
    "local_currency_code": "SGD",
    "budgets": {
        "b93bf281-5d2f-456a-961b-511da2682df6": {
            "category": "dining",
            "type": "Annual",
            "period": "072020",
            "budget_advise": "SGD 0/day",
            "budget_period": "01 Jan 2020 - 31 Dec 2020",
            "local_currency_amount_allowed": 100,
            "local_currency_period_spent": -860.82,
            "local_currency_period_remaining": -760.82,
            "created_at": "2020-06-30T16:20:51Z",
            "budget_notes": "status_above_100"
        },
        "d302d551-ec51-4516-9bc1-48de692b4abc": {
            "category": "dining",
            "type": "Monthly",
            "period": "072020",
            "budget_advise": "SGD 0/day",
            "budget_period": "01 Jul 2020 - 31 Jul 2020",
            "local_currency_amount_allowed": 100,
            "local_currency_period_spent": -537.48,
            "local_currency_period_remaining": -437.48,
            "created_at": "2020-06-30T16:23:20Z",
            "budget_notes": "status_above_100"
        }
    }
}
```

- `_id`: The pb_identifier of the user we are creating the budget for

- The keys of the "budgets" dictionary are the unique budget ids that the user has created.

- `category`: The transaction category that the user has created a budget for.

- `period`: The period at which the budget is created for. The period is the `%m%Y` format of when the budget was created. For example, if the user creates a budget on 5th Jul 2020, the period will be "072020".

- `budget_advise`: Contains the local_currency_code ("SGD") and amount (rounded to 0 d.p.)
the user is able to spend per day for the remaining days of the period. If the user creates a "Monthly" budget on 5th Jul 2020, the remaining days will be 6th Jul - 31st Jul 2020. If the user creates an "Annual" budget, the remaining days will be 6th Jul - 31st Dec 2020.

- `budget_period`: For "Monthly" budgets, this will be start to end of the month that the budget is created for. For annual budgets, it will be the start to end of the calendar year.

- `local_currency_amount_allowed`: The maximum amount the user is able to spend

- `local_currency_period_spent`: The amount the user has already spent

- `local_currency_period_remaining`: The remaining amount the user is able to spend

- `created_at`: The datetime that the budget was created at formatted in %Y-%m-%dT%H:%M:%SZ format.

- `budget_notes`: The current status of the budget. Either "status_above_100" and "status_below_100" will set if the user spent >= 100%/ < 100% of the maxmium amount he can spend respectively.


3. The following success or error message needs to be returned by the API if the budget has been successfully or unsuccessfully created.

```
{"status": "success", "message": "successfully created budget"}
{"status": "error", "message": "failed to create budget"}
```

4. The transactions of a given user from Apr 2020 - Jul 2020 has been provided below. The transactions of the user
should be stored in the "banks_users" collection of the M0 cluster mongodb database.

- `_id`: The pb_identifier of the user we are creating the budget for
- The keys of the "transactions" dictionary are the unique transaction ids for each of the transaction.
- `transacted_at`: The datetime at which the user made the transaction formatted in %Y-%m-%dT%H:%M:%SZ format.
- `description`: Meta description of what the transaction is made for.
- `category`: The transaction category of the transaction. This will be matched with the "category" of the budget.

```
{
    "_id": "16cecd11-2f83-4864-bf6b-f270f4be88cb",
    "local_currency_code": "SGD",
    "transactions": {
        "250773972570868310": {
            "base_currency_amount": -1.3,
            "base_currency_code": "SGD",
            "local_currency_amount": -1.3,
            "transacted_at": "2020-04-03T00:00:00Z",
            "description": "COLD STORAGE-BJ SINGAPORE SG",
            "category": "shopping"
        },
        "250773972570868311": {
            "base_currency_amount": -2.62,
            "base_currency_code": "SGD",
            "local_currency_amount": -2.62,
            "transacted_at": "2020-04-03T00:00:00Z",
            "description": "BUS/MRT 33803686 SINGAPORE SG",
            "category": "transfers"
        },
        "250773972570868312": {
            "base_currency_amount": -11.8,
            "base_currency_code": "SGD",
            "local_currency_amount": -11.8,
            "transacted_at": "2020-04-03T00:00:00Z",
            "description": "UNIQLO BUGIS+ SINGAPORE SG",
            "category": "shopping"
        },
        "250773972570868313": {
            "base_currency_amount": -4.32,
            "base_currency_code": "SGD",
            "local_currency_amount": -4.32,
            "transacted_at": "2020-04-05T00:00:00Z",
            "description": "POPULAR BOOK COMPANY-M SINGAPORE SG",
            "category": "education"
        },
        "250773972570868314": {
            "base_currency_amount": -50.29,
            "base_currency_code": "SGD",
            "local_currency_amount": -50.29,
            "transacted_at": "2020-05-05T00:00:00Z",
            "description": "SWENSEN'S-PWP SINGAPORE SG",
            "category": "shopping"
        },
        "250773972570868315": {
            "base_currency_amount": 271.86,
            "base_currency_code": "SGD",
            "local_currency_amount": 271.86,
            "transacted_at": "2020-05-07T00:00:00Z",
            "description": "GIRO PAYMENT",
            "category": "transfers"
        },
        "250773972570868316": {
            "base_currency_amount": -138.0,
            "base_currency_code": "SGD",
            "local_currency_amount": -138.0,
            "transacted_at": "2020-05-09T00:00:00Z",
            "description": "EU YAN SANG SINGAPORE SINGAPORE SG",
            "category": "personal_care"
        },
        "250773972579256925": {
            "base_currency_amount": -1.5,
            "base_currency_code": "SGD",
            "local_currency_amount": -1.5,
            "transacted_at": "2020-05-11T00:00:00Z",
            "description": "HAO MART - MANDARIN GA SINGAPORE SG",
            "category": "groceries"
        },
        "250773972579256926": {
            "base_currency_amount": 9.36,
            "base_currency_code": "SGD",
            "local_currency_amount": 9.36,
            "transacted_at": "2020-06-16T00:00:00Z",
            "description": "30CASHBACK",
            "category": "transfers"
        },
        "250773972579256927": {
            "base_currency_amount": -17.19,
            "base_currency_code": "SGD",
            "local_currency_amount": -17.19,
            "transacted_at": "2020-06-20T00:00:00Z",
            "description": "DELIVEROO SINGAPORE SG",
            "category": "shopping"
        },
        "250773972579256928": {
            "base_currency_amount": 614.87,
            "base_currency_code": "SGD",
            "local_currency_amount": 614.87,
            "transacted_at": "2020-06-21T00:00:00Z",
            "description": "PAYMENT - THANK YOU",
            "category": "income"
        },
        "250773972579256929": {
            "base_currency_amount": -46.53,
            "base_currency_code": "SGD",
            "local_currency_amount": -46.53,
            "transacted_at": "2020-06-07T00:00:00Z",
            "description": "FAIRPRICE FINEST-MARIN SINGAPORE SG",
            "category": "groceries"
        },
        "250773972579256930": {
            "base_currency_amount": 63.72,
            "base_currency_code": "SGD",
            "local_currency_amount": 63.72,
            "transacted_at": "2020-07-05T00:00:00Z",
            "description": "PAYMENT - THANK YOU",
            "category": "transfers"
        },
        "250773972579256931": {
            "base_currency_amount": -33.89,
            "base_currency_code": "SGD",
            "local_currency_amount": -33.89,
            "transacted_at": "2020-07-05T00:00:00Z",
            "description": "DELIVEROO SINGAPORE SG",
            "category": "shopping"
        },
        "250773972579256932": {
            "base_currency_amount": -55.27,
            "base_currency_code": "SGD",
            "local_currency_amount": -55.27,
            "transacted_at": "2020-07-05T00:00:00Z",
            "description": "DELIVEROO SINGAPORE SG",
            "category": "shopping"
        },
        "250773972579256933": {
            "base_currency_amount": 33.89,
            "base_currency_code": "SGD",
            "local_currency_amount": 33.89,
            "transacted_at": "2020-07-05T00:00:00Z",
            "description": "PAYMENT - THANK YOU",
            "category": "transfers"
        },
        "250773972587645542": {
            "base_currency_amount": -13.65,
            "base_currency_code": "SGD",
            "local_currency_amount": -13.65,
            "transacted_at": "2020-07-06T00:00:00Z",
            "description": "NTUC FP-BEDOK B SINGAPORE SG",
            "category": "groceries"
        },
        "250773972587645543": {
            "base_currency_amount": 2.5,
            "base_currency_code": "SGD",
            "local_currency_amount": 2.5,
            "transacted_at": "2020-07-06T00:00:00Z",
            "description": "30CASHBACK",
            "category": "transfers"
        },
        "250773972587645544": {
            "base_currency_amount": -10.5,
            "base_currency_code": "SGD",
            "local_currency_amount": -10.5,
            "transacted_at": "2020-07-06T00:00:00Z",
            "description": "HOMEGROUND COFFEE ROAS SINGAPORE SG",
            "category": "shopping"
        }
    }
}
```