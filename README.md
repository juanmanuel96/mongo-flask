# MongoFlask
A Python Flask library for connecting a MongoDB instance to a Flask application.

## Installation
Module is not available in PyPI yet. However, you can install it with pip with the following command via ssh:
```
pip install git+ssh://git@github.com/juanmanuel96/mongo-flask.git
```
To install via HTTPS:
```
pip install git+https://git@github.com/juanmanuel96/mongo-flask.git
```

## Application Configuration
Upon creation of the application, you need to set the following Flask application configuration variables:
1. `MONGO_HOST` = MongoDB connection host IP or domain. **Required**
2. `MONGO_PORT` = MongoDB connection port. **Required**
3. `MONGO_DATABASE` = MongoDB database of the application **Required**
4. `MONGO_USER` = MongoDB connection username (optional)
5. `MONGO_PWD` = MongoDB connection password (optional) 
**NOTE:** If `MONGO_USER` is provided, `MONGO_PWD` will be required.

## Quick Start
This section details a quick start to the MongoFlask class.
```python
from flask import Flask, render_template
from mongo_flask import MongoFlask
from mongo_flask.core.collections import CollectionModel
from mongo_flask.code.fields import StringField

class MyCollection(CollectionModel):
    collection_name = 'my_collection'
    field1 = StringField()
    

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DATABASE'] = 'my_database'

mongo = MongoFlask(app)
mongo.register_collection(MyCollection)


@app.route('/')
def index():
    collection = mongo.get_collection('my_collection')
    document_set = collection.all()
    return render_template('index.html', document_set=document_set)
``` 

## Using MongoFlask
The MongoFlask class can be instantiated as `mongo = MongoFlask`. To connect the instance to a Flask app, it can be 
done by passing the application as a parameter of MongoFlask or by calling the `MongoFlask.init_app` method and passing 
the Flask application as parameter. After MongoFlask has been instantiated and a Flask app has been connected, proceed 
by creation collection DRM object. 

### Creating a Collection DRM object
This package implements a sort of ORM which we call DRM, Document Relational Mapping. A DRM object is a representation 
a database collection. Usually it should have the same name as the collection, but it is not a requirement. However, 
it should have a `collection_name` attribute which should be the name of the collection in the database as-is. here is 
how you can create a Collection DRM object.
```python
from mongo_flask.core.collections import CollectionModel
from mongo_flask.core.fields import StringField, IntegerField

class MyCollection(CollectionModel):
    collection_name = 'my_collection'
    name = StringField(required=True, max_lenght=50)
    age = IntegerField()
```
When the Collection DRM object has been created, it should be registered in the `MongoFlask` instance for use.

### Registering a collection
In the same file where `MongoFlask` was instantiated, call the method `register_collection` and pass the collection 
class (not instance), as parameter.
```python
mongo.regsiter_collection(MyCollection)
```

### Retrieving a collection for use
To retrieve a collection DRM, you may do this by using the `MongoFlask` instance directly, or through the Flask app, 
and calling the `get_collection` method. This method expects the collection name as parameter (not the collection 
class).  
```python
# To retrieve from the MongoFlask instance
collection = mongo.get_collection('my_collection')

# To retrieve from the Flask app
app.mongo.get_collection('my_collection')
```

## For further documentation
Documentation on the class is being developed.

