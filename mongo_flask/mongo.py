from flask import Flask
from .core.wrappers import MongoConnect, MongoDatabase
from .core.collections import BaseCollection
from .errors import DatabaseException, CollectionException, CollectionInvalid


class MongoFlask(object):
    def __init__(self, app=None):
        """
        Connect your MongoDB client to a Flask application. The MongoFlask object
        has 3 attributes: client, db, and collection.
        1. `client` is the MongoDB instance in the computer.
        2. `db` is the Database to connect to.
        3. `collections` is a map of the collections of the DB

        :param app: Instance of your application
        :type app: Flask

        ## Change log
        |Version|Description|
        |-------|-----------|
        |v0.01  |Initial release of API|
        |v0.02  |Changes for ease of use|
        """
        self.__client = None  # MongoDB client
        self.__db = None  # Application database
        self.__collections = {}  # Database collections

        if app is not None:
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
        host = app.config.get('MONGO_HOST', 'localhost')
        port = app.config.get('MONGO_PORT', 27017)
        username = app.config.get('MONGO_USER', None)
        pwd = app.config.get('MONGO_PWD', None)
        db_name = app.config.get('MONGO_DATABASE', None)

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
        # self.collections = self.__collections__()
    
    # def __collections__(self):
    #     """
    #     Retrieves Collections in DB and inserts into collections attribute. If
    #     there are no collections, returns empty `dict`. Otherwise, creates a `dict`
    #     object with instances of the collections.
    #     """
    #     collections = self.db.list_collection_names()
    #     if len(collections) == 0:
    #         return {}
    #     else:
    #         col_dict = {}
    #         for collection in collections:
    #             col_dict[collection] = MongoCollection(self.db, collection)
    #         return col_dict

    def register_collection(self, collection_cls):
        """
        Collection is a user-defined collection that will be added to the MongoFlask instance
        """
        if issubclass(collection_cls, BaseCollection):
            self.__register_collection(collection_cls)
        else:
            raise Exception('Only Collection classes are valid')

    def __register_collection(self, collection_cls):
        _name = collection_cls.collection_name
        _collection = collection_cls(self.db, _name)
        _collection.__client__session__ = self.__client.start_session
        success = self.__update_collections__(_name, collection_cls)
        if not success:
            raise Exception('Something happened')
        self.__update_app()

    def __update_app(self):
        try:
            from flask import current_app
            current_app.mongo = self
        except RuntimeError as run_err:
            """This app is not a Flask app, continuing without problems"""
        except Exception as err:
            """Something else happened, figure it out"""

    def __update_collections__(self, name, collection_cls):
        self.__collections.update({name: collection_cls})
        return self.collections.get(name) is not None

    # def insert_collection(self, collection_name = None):
    #     """
    #     Inserts a new collection into the collections attribute. If collection does not
    #     exists, it is created.
    #
    #     :param collection_name: Name of the collection to be inserted
    #     :param collection_name: str
    #     """
    #     if collection_name is None:
    #         raise CollectionException()
    #
    #     try:
    #         self.collections[collection_name] = MongoCollection(self.db, collection_name, create=True)
    #     except OperationFailure:
    #         self.collections[collection_name] = MongoCollection(self.db, collection_name)
    #     return True
    
    def get_collection(self, collection_name=None) -> BaseCollection:
        """
        Retrieves a Collection instance from the collections attribute.

        :param collection_name: Name of the collection to be retrieved
        :type collection_name: str
        """
        if not collection_name:
            raise CollectionException(
                message='A collection name is required'
            )

        if self.collections.get(collection_name) is None:
            raise CollectionInvalid()
        else:
            return self.collections.get(collection_name)
