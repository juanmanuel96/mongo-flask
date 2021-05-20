from flask import Flask
from pymongo.errors import OperationFailure

from .core.wrappers import MongoConnect, MongoDatabase
from .core.collections import CollectionModel
from .errors import DatabaseException, CollectionException, CollectionInvalid, InvalidClass, RegistrationException, \
    URIMissing


class MongoFlask(object):
    def __init__(self, app=None):
        """
        Connect your MongoDB client to a Flask application. The MongoFlask object
        has 3 attributes: client, db, and collection.
        1. `client` is the MongoDB instance in the computer.
        2. `db` is the Database to connect to.
        3. `collections` is a map of the collections of the DB

        ## Change log
        |Version|Description|
        |-------|-----------|
        |v0.01  |Initial release of API|
        |v0.02  |Changes for ease of use|
        """
        self.__client = None  # MongoDB client
        self.__db = None  # Application database
        self.__collections = {}  # Database collections

        if app:
            # App is initialized if sent as parameter else, init_app 
            # has to be called
            self.init_app(app)

    @property
    def client(self):
        return self.__client

    @property
    def db(self):
        return self.__db

    @property
    def collections(self):
        return self.__collections

    def init_app(self, app):
        """
        Initializes the application. Flask instance MUST have at least the 
        MONGO_HOST, MONGO_PORT, and MONGO_DATABASE in the application configuration. 
        Username and password are optional. If database name is provided, it is also 
        initialized.

        :param app: Flask instance of the application
        :type app: Flask
        """
        host = app.config.get('MONGO_HOST')
        port = app.config.get('MONGO_PORT')
        username = app.config.get('MONGO_USER')
        pwd = app.config.get('MONGO_PWD')
        db_name = app.config.get('MONGO_DATABASE')

        if not host or not port:
            raise URIMissing(
                message=f'MONGO_HOST and MONGO_PORT cannot be "{type(None)}"',
                fix='Provide a valid MONGO_HOST and MONGO_PORT value'
            )

        account = f'{username}:{pwd}@' if username and pwd else ''
        conn = f'{host}:{port}'
        uri = f'mongodb://{account}{conn}'
        
        self.__client = MongoConnect(uri)
        self.__database__(db_name)
        
        if isinstance(app, Flask):  # Makes the package available to non-Flask projects
            app.mongo = self  # Create mongo attribute in Flask instance

    def __database__(self, db_name=None):
        """
        Sets the db attribute of the object.

        :param db_name: Name of the database to connect to
        :type db_name: str
        """
        if db_name is None:
            raise DatabaseException()

        self.__db = MongoDatabase(self.client, db_name)

    def register_collection(self, collection_cls):
        """
        Collection is a user-defined collection that will be added to the MongoFlask instance
        """
        if issubclass(collection_cls, CollectionModel):
            return self.__register_collection(collection_cls)
        else:
            raise InvalidClass(collection_cls)

    def __register_collection(self, collection_cls):
        _name = collection_cls.collection_name
        _collection, success = self._insert_collection(_name, collection_cls)
        _collection.client_session = self.__client.start_session
        if not success:
            raise RegistrationException()
        self.__update_app()
        return success

    def _insert_collection(self, name, collection_cls: CollectionModel):
        """
        Inserts a new collection into the collections attribute. If collection does not
        exists, it is created.
        """
        try:
            _collection = collection_cls(self.db, create=True)
        except OperationFailure:
            _collection = collection_cls(self.db)
        self.__collections.update({name: _collection})
        return _collection, self.collections.get(name) is not None

    def __update_app(self):
        try:
            from flask import current_app
            current_app.mongo = self
        except RuntimeError as run_err:
            """This app is not a Flask app, continuing without problems"""
            pass
    
    def get_collection(self, collection_name=None) -> CollectionModel:
        """
        Retrieves a Collection instance from the collections attribute.

        :param collection_name: Name of the collection to be retrieved
        :type collection_name: str
        """
        if not collection_name:
            raise CollectionException(message='A collection name is required')

        collection_to_return = self.collections.get(collection_name)
        if not collection_to_return:
            raise CollectionInvalid()
        return collection_to_return
