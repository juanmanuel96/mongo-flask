# Mongo-Flask
A Python Flask library for connecting a MongoDB instance to the Flask application.

## Why I made this package
This package was inspired by he package **[Flask-PyMongo](https://github.com/dcrosta/flask-pymongo)** and **[Flask-Login](https://github.com/maxcountryman/flask-login)**. I wanted to create package which would connect a Flask application to a MongoDB instance and have a proxy class like `current_app` from Flask or `current_user` from Flask-Login to make use of the DB from anywhere in the application. The latter is still in development.

## How to use
Module is not available in pip yet. You will need to download the source code. Copy the `mongo-flask` package under `yourapplication` folder. From there on out, just call the MongoFlask class in your application.

### Application Configuration
Upon creation of the application, you need to set the following application config variables:
1. MONGO_USER = MongoDB connection username (optional)
2. MONGO_PWD = MongoDB connection password (optional)
3. MONGO_HOST = MongoDB connection host IP or domain. **Required**
4. MONGO_PORT = MongoDB connection port. **Required**

### Client Instantiation
After application instantiation and setting configurations, instantiate your MongoDB client as follows:
```python
from .mongo_flask import MongoFlask
mongo_flask = MongoFlask(app) # Set the MongoFlask client instance
mongo_flask.set_Database(db_name='db_name') # Set the database attribute
```
You may also do as follows:
```python
from .mongo_flask import MongoFlask
mongo_flask = MongoFlask(app, 'db_name') # Sets client instance and DB instance
```

### How to use the Database attribute
Now that the client has bee instantiated, the next step is to use the database attribute to call collections. To use the database attribute, do as follows:
```python
from flask import current_app

collection = current_app.mongo.database['collection']
docs = collection.find()
```

### Methods to get a Collection
The MongoFlask instance has an attribute called collections. This attribute is a dictionary where the keys
are the collection names and their values are the Collection instances. To use the methods on the Collection
class, retrieve the Collection instance the same way your would retrieve the value of a key froma disctionary.
For example:
```python
from flask import current_app

collection = current_app.mongo.collections.get('collction_name')
docs = collection.find()
```
Another method:
```python
from flask import current_app
collection = current_app.mongo.get_collection('collection_name')
docs = collection.find()
```
