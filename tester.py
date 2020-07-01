from mongo_flask import MongoFlask
import pytest
from flask import Flask
from mongo_flask.exceptions import *
from mongo_flask.wrappers import MongoConnect, MongoDatabase, MongoCollection

app = Flask(__name__)
mongo = MongoFlask()

def app_config(temp=app, host='localhost', port='27017', db_name='mongo_flask', init=False):
    temp.config['MONGO_HOST'] = host
    temp.config['MONGO_PORT'] = port
    temp.config['MONGO_DATABASE'] = db_name
    if init:
        mongo.init_app(temp)

#######################################
# Tests
#######################################
# Testing Exceptions
def test_missing_complete_uri():
    app_config(host=None, port=None, db_name=None)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_host():
    app_config(host=None)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_port():
    app_config(port=None,)
    with pytest.raises(URIMissing):
        mongo.init_app(app)

def test_missing_database():
    app_config(db_name=None)
    with pytest.raises(DatabaseException):
        mongo.init_app(app)

# Testing MongoFlask attributes types
def test_client_type():
    app_config(init=True)
    assert type(mongo.client) == type(MongoConnect())

def test_database_type():
    app_config(init=True)
    assert type(mongo.db) == type(MongoDatabase())

def test_collection_type():
    app_config(init=True)
    assert type(mongo.collections) == type(dict())

# Testing collection methods
def test_get_collection():
    app_config(init=True)
    collection = mongo.get_collection('testing')
    assert collection.name == 'testing'

def test_get_collection_fail():
    app_config(init=True)
    with pytest.raises(CollectionInvalid):
        mongo.get_collection('invalid_col')

def test_insert_collection():
    app_config(init=True)
    ack = mongo.insert_collection('testing2')
    assert ack == True