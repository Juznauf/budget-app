# Manual documentation for api

## Feature list

* `main.py` should handle the initialization of the api, as well as calling the modules to route the path operations for user operations

* path operation to handle user budget request with the following fields(`'pb_identifier'`,`category`, `amount`, `budget_type`)
    * path operation should be in router under the user request
    * request should be a `POST` request
    * ideally there should be no default params
    * once data has been validated, will call on a function from `budget.py`
    * should be able to update the DB with this info once validated, db operation in next feature

* DB operations for creation of budgets
    * ideally should have a db operation that sends data to our database 
    * no need to do AUTH as we have to only showcase the functionality of the API in creating the budgets [notes: did autho with OAuth2 instead] *done*
    * use `pymongo` to establish a connection to our database *done* 
    * use pydantic to validate our user login form before we start routing, validate if name exist in the database collections [notes: decided to use OAuth2 instead] *done*  
    * A document (`JSON`) needs to be created in a `"plannerbee"` database, under the `"budget_users"` collection of our M0 cluster mongodb database. The schema should follow the schema given in [readme](README.md) *done*
    * if document has been succesfully created then our user path operator will return a message, else raise an error
    * updating operation for the creation of user budgets

* `router.py` can handle standard OAuth2 however with no proper securitization, we have just set the username lookup, if username not in `db.collection`s then will raises a `HTTPException`. Taken reference for security from [here](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/). [notes: initially tried validating through form data however received `"GET /login/ HTTP/1.1" 405 Method Not Allowed`, additionally authorization can only be done in the docs as we havent added a proper JWT authentication, alternatively can use [simple auth](https://fastapi.tiangolo.com/advanced/security/http-basic-auth/)] *done*


* Should have a `GET` request for the user in the user path operator to view the successfully created budgets

## Issues

* `TypeError: Object of type 'ModelMetaclass' is not JSON serializable` encountered earlier as we tried to pass the function parameters of our response model through the body of our path function. Was resolved by passing the function parameters of our response model through our path operator function params.

## Queries

* For the budget keys, do we have to create them ourselves?


## References
* For data validation using pydantic look [here](https://pydantic-docs.helpmanual.io/usage/models/)
