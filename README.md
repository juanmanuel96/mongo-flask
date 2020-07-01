# Mongo-Flask
A Python Flask library for connecting a MongoDB instance to the Flask application.

## Why I made this package
This package was inspired by he package **[Flask-PyMongo](https://github.com/dcrosta/flask-pymongo)** and **[Flask-Login](https://github.com/maxcountryman/flask-login)**. I wanted to create package which would connect a Flask application to a MongoDB instance and have a proxy class like `current_app` from Flask or `current_user` from Flask-Login to make use of the DB from anywhere in the application. The latter is still in development.

## How to use
Module is not available in pip yet. You will need to download the source code. Copy the `mongo-flask` package under `yourapplication` folder. From there on out, just call the MongoFlask class in your application.

### Application Configuration
Upon creation of the application, you need to set the following Flask application configuration variables:
1. MONGO_HOST = MongoDB connection host IP or domain. **Required**
2. MONGO_PORT = MongoDB connection port. **Required**
3. MONGO_DATABASE = MongoDB database of the application **Required**
4. MONGO_USER = MongoDB connection username (optional)
5. MONGO_PWD = MongoDB connection password (optional) 
**NOTE:** If MONGO_USER is provided, MONGO_PWD will be required.

### Quick Start to MongoFlask
This section details a quick start to the MongoFlask class.
```python
from flask import Flask, render_template
from mongo_flask import MongoFlask

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DATABASE'] = 'my_database'

mongo = MongoFlask(app)
mongo.insert_collection('my_collection')

@app.route('/')
def index():
    collection = mongo.get_collection('my_collection')
    docs = collection.list_find()
    return render_template('index.html', docs=docs)
```
You can also use the `current_app` proxy class of Flask to use the MongoFlask instance as `current_app.mongo`. 

### Methods to get a Collection
The MongoFlask instance has an attribute called collections. This attribute is a dictionary where the keys are the collection names and their values are the Collection instances. The following are methods to retrieve a collection from the MongoFlask instance.
1. Using the `get_collection()` method from the `MongoFlask` class . **Recommended**
```python
collection = current_app.mongo.get_collection('collection_name')
docs = collection.find()
``` 
2. Using the `get()` method from the `dict()` class.
```python
collection = current_app.mongo.collections.get('collction_name')
docs = collection.find()
``` 
3. Using dictonary brackets.
```python
collection = current_app.mongo.collections['collection_name']
docs = collection.find()
```
4. Using the `db` attribute.
```python
collection = current_app.mongo.db['collection_name']
docs = collection.find()
```
There are many more methods you can use to retrieve a collection from MongoFlask, it is up to you on which one you prefer. Refer to the methods doctrings for more information.
