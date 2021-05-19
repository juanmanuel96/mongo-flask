import pytest
from flask import Flask

from mongo_flask import MongoFlask
from mongo_flask.core.wrappers import MongoConnect, MongoDatabase
from mongo_flask.core.collections import CollectionModel
from mongo_flask.core.fields import StringField, IntegerField
from mongo_flask.core.document import Document, DocumentSet
from mongo_flask.errors.exceptions import *

app = Flask(__name__)
mongo = MongoFlask()


class Testing(CollectionModel):
    # A Collection that has records
    collection_name = 'testing'
    doc_num = StringField(required=True)
    desc = StringField()


class Testing2(CollectionModel):
    # An existing empty collection
    collection_name = 'testing2'
    first_name = StringField()
    last_name = StringField()
    age = IntegerField()


class Testing3(CollectionModel):
    # A collection that does not exist
    collection_name = None
    first_name = StringField()
    last_name = StringField()
    height = IntegerField()


class AnInvalidCollection:
    # The name says it all
    collection_name = 'i_am_invalid'
    a_name_field = StringField()


def app_config(temp=app, host='localhost', port='27017', db_name='mongo_flask', init=True):
    temp.config['MONGO_HOST'] = host
    temp.config['MONGO_PORT'] = port
    temp.config['MONGO_DATABASE'] = db_name
    if init:
        mongo.init_app(temp)
    return temp


def register_collection_for_test(collection_cls=Testing):
    mongo.register_collection(collection_cls)


#######################################
# Tests
#######################################
# Testing connection to database
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
    assert isinstance(app.mongo, MongoFlask)


def test_client_type():
    app_config()
    assert isinstance(mongo.client, MongoConnect)


def test_database_type():
    app_config()
    # Will use the MongoFlask instance client since it is required
    # to instantiate MongoDatabase
    assert isinstance(mongo.db, MongoDatabase)


def test_collection_type():
    app_config()
    assert isinstance(mongo.collections, dict)


# Testing MongoFlask methods
def test_collection_registration():
    app_config()
    mongo.register_collection(Testing)


def test_collection_registration_empty():
    app_config()
    mongo.register_collection(Testing2)


def test_collection_registration_not_in_db():
    app_config()
    with pytest.raises(CollectionException):
        mongo.register_collection(Testing3)


def test_collection_registration_invalid():
    app_config()
    with pytest.raises(InvalidClass):
        mongo.register_collection(AnInvalidCollection)


def test_get_collection():
    app_config()
    register_collection_for_test()
    collection = mongo.get_collection('testing')
    assert isinstance(collection, CollectionModel)


def test_get_collection_without_name():
    app_config()
    register_collection_for_test()
    with pytest.raises(CollectionException):
        mongo.get_collection()


def test_get_collection_does_not_exist():
    app_config()
    register_collection_for_test()
    with pytest.raises(CollectionInvalid):
        mongo.get_collection('not_a_good_collection_name')


# Collection level operation tests
def test_collection_method_all():
    app_config()
    register_collection_for_test()
    collection = mongo.get_collection('testing')
    docu_set = collection.all()
    assert isinstance(docu_set, DocumentSet)


def test_collection_method_all_correct_document_set_length():
    """
    This is a very specific test with a very specific length for the DocumentSet object. The purpose is to confirm
    that it is returning a DocumentSet object and that the length of the object matches the amount of documents in the
    'testing' collection. Later tests will validate the content of these documents.
    """
    app_config()
    register_collection_for_test()
    collection = mongo.get_collection('testing')
    docu_set = collection.all()
    assert len(docu_set) == 350


def test_collection_method_filter():
    app_config()
    register_collection_for_test()
    collection = mongo.get_collection('testing')
    docu_set = collection.filter(desc='this is a test document')
    assert isinstance(docu_set, DocumentSet) and isinstance(docu_set[0].desc, StringField)


def test_collection_method_get():
    app_config()
    register_collection_for_test()
    collection = mongo.get_collection('testing')
    document = collection.get(doc_num='doc0')
    assert isinstance(document, Document)


def test_collection_method_get_empty():
    app_config()
    register_collection_for_test(Testing2)
    collection = mongo.get_collection('testing2')
    document = collection.get()  # Empty get should return Document object with empty fields
    assert isinstance(document, Document)
