### REST API architecture




### FastAPI notes

#### Trying out the tutorial from FastAPI

Tutorial can be found [here](https://fastapi.tiangolo.com/tutorial/)

Install FastAPI with all the optional dependencies
```
pip install fastapi[all]
```

This installs `uvicorn` as well which we will use as a server

Run the server with 
```
uvicorn main:app --reload
```
The reload flag will make the server restart after code changes. The `app` refers to the namespace given to the instance of the FastAPI in the `main.py`. 

To see the interactive docs. Go to `root/docs`. To see the alternative docs go to `root/redoc`.

To see the raw OpenAPI scheme, go to `root/openapi.json`.

For the various HTTP request methods, uvicorn gives us the following:
```
POST: to create data
GET: to read data
PUT: to update data
DELETE: to delete data
```
**path functions**

For the functions define to our paths, we use the `async` statement together with the `wait` statements to allow for concurrency in the API requests.


The path functions also allow us to use standard python type annotations. 

for eg.
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```
if the value passed to item_id is not an int, then a http error will be raised. This allows for data validation when passing values. This is enabled with the use of pydantic. 

Path declarations are called in order, so the path extensions must be written in order.

for eg.

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```


If we want predefined path params then do this:

```python

from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
```
Notice that for the function params, we need to indicate the type params, so that it can check against the class which we have created, if the class is not the same then a HTTP error will be raised. For the get method, the items pass will be in a dictionary so we can check the get method value with `model_name.value` for the above example.

For the above example say the path is `root/model/alexnet`, then in the client the response is 
```json
{
    "model_name": "alexnet",
    "message": "Deep Learning FTW!"
}
```

**query parameters**

When you declare other function parameters that are not part of the path parameters, they are automatically interpreted as "query" parameters.


```python
from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```
The query is the set of key-value pairs that go after the `?` in a URL, separated by `&` characters.

If we declare the values in our path functions as a type, then they are converted to that type and validated against it. 


We can also declare optional query params, by setting their default to `None`:

for eg,
```python
from typing import Optional

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```
The Optional in `Optional[str]` is not used by FastAPI (FastAPI will only use the str part), but the `Optional[str] `will let your editor help you finding errors in your code.

We can declare multiple path parameters and query parameters at the same time, FastAPI knows which is which

for eg.
```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
```










### MongoDB Atlas 

Getting started using this [tutorial](https://towardsdatascience.com/getting-started-with-mongodb-atlas-overview-and-tutorial-7a1d58222521) 

