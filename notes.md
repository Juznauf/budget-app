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


**request body**

When you need to send data from a client, to the API, you send it as a request body. A request body is sent by the client to your API. A response body is the data your API sends to the client. Your API almost always has to send a response body. But clients don't necessarily need to send request bodies all the time. To declare a request body, you use Pydantic models with all their power and benefits  


Import the Basemodel from pydantic

```python
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
```

To add the item to the path operation, declare it the same way we declared path and query params


We can also add additional validation for optional params with Query, as such

```python
from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

we can also add regex to the Query params for additional validation 

When we need to declare a value as required while using Query, you can use `...` (the python elipsis params) as the first argument as such 

```python

@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

We can also declare it to recieve a list of values such as 

```python
from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
```

now using a get request we can have multiple q as our parameters
The response to the above url is 
```json
{
  "q": [
    "foo",
    "bar"
  ]
}
```


Difference between using `list` and `List[int]` is that the latter would check the contents of list as all being integers and the former would not.


**Alot of fastAPI revolves around the fact that data validation should be done in the function header instead of the body of the function, such that we can send the response errors can be automated






### MongoDB Atlas 

MongoDB is a nosql database. It supports various forms of data. MongoDB stores data in JSON like documents, which makes the database very flexible and scalable.
MongoDB is a document-oriented database model. Each MongoDB database contains collections and which in turn contains documents. Each document can be different and depends on the varying number of fields.  The model of each document will be different in size and content from each other. The data model features allow you to store arrays and complex structured in a hierarchical relationship.


Getting started using this [tutorial](https://towardsdatascience.com/getting-started-with-mongodb-atlas-overview-and-tutorial-7a1d58222521) 

Charactheristics of MongoDB, from [here](https://www.educba.com/mongodb-nosql/)
* Schema-Less
    * It has no schema so it can have many fields, content, and size different than another document in the same collection.
* Indexing
    * Indexing is very important for improving the performances of search queries. MongoDB uses indexing of dataset to enhance query performances and searches.  MongoDB indexing enhances the performance for the faster search query. Document in a MongoDB can be used for indexing using primary and secondary indices.
* File storage
    * Can be used as a file system with load balancing and data replication features over multiple machines for storing files.
* Replication
    * The feature of replication is to distribute data multiple nodes. It can have primary nodes and secondary nodes to replicate data. Replication of data is done using master-slave architecture. MongoDB provides a replication feature by distributing data across multiple machines.
* Sharding 
    * This process distributes data across multiple physical partitions called shards. Due to sharding MongoDB automatic process load balancing. We use sharding in cases where we need to work on very larger datasets.


#### Using Mongodb with fastapi

Tutorial [here](https://frankie567.github.io/fastapi-users/configuration/databases/mongodb/#next-steps)


For the driver will use the [Pymongo](https://docs.mongodb.com/drivers/pymongo) driver instead of motor, as motor does not support windows.

To connect to our mongodb cluster see [this](https://docs.atlas.mongodb.com/tutorial/connect-to-your-cluster/)




### The hierarchy of fastapi

see [here](https://fastapi.tiangolo.com/benchmarks/)