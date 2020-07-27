# Manual documentation for api

## Instructions on running the api

1. While in the `app` directory. Run the following command in shell `uvicorn main:app --reload`
2. Go to the relative path `root\docs`
3. Click on `authorize`, enter the following user `16cecd11-2f83-4864-bf6b-f270f4be88cb` in the username and for the password put in any character
4. Once authorized, the user can then utilise the api under the current user id

## Feature list

* `main.py` should handle the initialization of the api, as well as calling the modules to route the path operations for user operations *`done`*

* path operation to handle user budget request with the following fields(`'pb_identifier'`,`category`, `amount`, `budget_type`)
    * path operation should be in router under the user request *`done`*
    * request should be a `POST` request *`done`*
    * once data has been validated, will call on a function from `budget.py` *`done`* 
    * should be able to update the DB with this info once validated, db operation in next feature *`done`*

* DB operations for creation of budgets
    * ideally should have a db operation that sends data to our database *`done`* 
    * no need to do AUTH as we have to only showcase the functionality of the API in creating the budgets [notes: did autho with OAuth2 instead] *`done`*
    * use `pymongo` to establish a connection to our database *`done`* 
    * use pydantic to validate our user login form before we start routing, validate if name exist in the database collections [notes: decided to use OAuth2 instead] *`done`*  
    * A document (`JSON`) needs to be created in a `"plannerbee"` database, under the `"budget_users"` collection of our M0 cluster mongodb database. The schema should follow the schema given in [readme](README.md) *`done`*
    * if document has been succesfully created then our user path operator will return a message, else raise an error [notes: will not raise any errors, errors could be due to a number of things in the budget module as well as db connection] *`done`*
    * updating operation for the creation of user budgets *`done`*
    * need to also check if an existing budget alr exist in our db *`done`*

* `router.py` can handle standard OAuth2 however with no proper securitization, we have just set the username lookup, if username not in `db.collection`s then will raises a `HTTPException`. Taken reference for security from [here](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/). [notes: initially tried validating through form data however received `"GET /login/ HTTP/1.1" 405 Method Not Allowed`, additionally authorization can only be done in the docs as we havent added a proper JWT authentication, alternatively can use [simple auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/)] *`done`*


* Should have a `GET` request for the user in the user path operator to view the successfully created budgets *`done`*

## Issues

* `TypeError: Object of type 'ModelMetaclass' is not JSON serializable` encountered earlier as we tried to pass the function parameters of our response model through the body of our path function. Was resolved by passing the function parameters of our response model through our path operator function params.

* nested objects when querying has to be specified by dot notation

## Assumptions

* Currency is denoted as floating point numbers and not integers
* The day that the budget is created is not counted in the remaining days to spend 

## References
* For data validation using pydantic look [here](https://pydantic-docs.helpmanual.io/usage/models/)


