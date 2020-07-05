from mongo_flask import MongoFlask, DESCENDING
import pytest
from flask import Flask
from mongo_flask.exceptions import *
from mongo_flask.wrappers import MongoConnect, MongoDatabase, MongoCollection

app = Flask(__name__)
mongo = MongoFlask()

def app_config(temp=app, host='localhost', port='27017', db_name='mongo_flask', init=True):
    temp.config['MONGO_HOST'] = host
    temp.config['MONGO_PORT'] = port
    temp.config['MONGO_DATABASE'] = db_name
    if init:
        mongo.init_app(temp)

def insert_documents(collection, amount=1):
    for i in range(0, amount):
        doc = {'doc_num' : f'doc{i}', 'desc' : 'this is a test document'}
        collection.insert_one(doc)

def delete_documents(collection):
    collection.delete_many({})

#######################################
# Tests
#######################################
# Testing Exceptions
def test_missing_complete_uri():
    app_config(host=None, port=None, db_name=None, init=False)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_host():
    app_config(host=None, init=False)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_port():
    app_config(port=None, init=False)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_database():
    app_config(db_name=None, init=False)
    with pytest.raises(DatabaseException):
        mongo.init_app(app)

# Testing MongoFlask attributes types
def test_app_mongo():
    app_config()
    assert type(app.mongo) == type(MongoFlask())

def test_client_type():
    app_config()
    assert type(mongo.client) == type(MongoConnect())

def test_database_type():
    app_config()
    # Will use the MongoFlask instance client since it is required
    # to instantiate MongoDatabase
    assert type(mongo.db) == type(MongoDatabase(mongo.client, 'mongo_flask'))

def test_collection_type():
    app_config()
    assert type(mongo.collections) == type(dict())

# Testing collection methods
def test_get_collection():
    app_config()
    collection = mongo.get_collection('testing')
    assert collection.name == 'testing'

def test_get_collection_fail():
    app_config()
    with pytest.raises(CollectionInvalid):
        mongo.get_collection('invalid_col')

def test_insert_collection():
    app_config()
    ack = mongo.insert_collection('testing2')
    assert ack == True

def test_list_find():
    app_config()
    collection = mongo.get_collection('testing')
    insert_documents(collection, 100)
    docs = collection.list_find()
    delete_documents(collection)
    assert type(docs) == type(list())

def test_find_amount_0():
    app_config()
    collection = mongo.get_collection('testing2')
    insert_documents(collection, 250)
    docs = collection.find_first_amount(amount=5)
    delete_documents(collection)
    assert len(docs) == 5

def test_find_amount_1():
    app_config()
    amount = 235
    collection = mongo.get_collection('testing2')
    insert_documents(collection, 500)
    docs = collection.find_first_amount(amount=amount)
    delete_documents(collection)
    assert len(docs) == amount

def test_descending_sorting():
    app_config()
    collection = mongo.get_collection('testing')
    insert_documents(collection, 350)
    docs = collection.find().sort('doc_num', DESCENDING)
    assert docs[349]['doc_num'] == 'doc0'

