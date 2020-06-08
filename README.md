# Mongo-Flask
A Python Flask library for connecting a MongoDB instance to the application.

## How to use
Module is not available in pip yet. You will need to download the source code. Copy the `mongo-flask` package under 
`yourapplication` folder. From there on out, just call the MongoFlask class in your application.

### Application Configuration
Upon creation of the application, you need to set the following application config variables:
1. MONGO_USER = MongoDB connection username (optional)
2. MONGO_PWD = MongoDB connection password (optional)
3. MONGO_HOST = MongoDB connection host IP or domain. Defaults to 'localhost'
4. MONGO_PORT = MongoDB connection port. Defaults to '27017'

### Client Instantiation
After application instantiation and setting configurations, instantiate your MongoDB client as follows:
```python
from .mongo_flask import MongoFlask
mongo_flask = MongoFlask(app) # Set the MongoFlask client instance
mongo_flask.set_Database(db_name='db_name') # Set the database attribute
```

### How to use the Database attribute
Now that the client has bee instantiated, the next step is to use the database attribute to call collections.
To use the database attribute, do as follows:
```python
from flask import current_app

collection = current_app.mongo_flask.database['collection']
docs = collection.find()
```

### Another method to set and use collections
Another method to set the Collection to use at the moment, do as follows:
```python
from flask import current_app

collection = current_app.mongo_flask.set_Collection(collection_name='collection')
docs = collection.find()
```
It is not recommended to do this in the `__init__.py` file because the Collection 
can change from operation to operation.
