from .wrappers import MongoConnect, MongoDatabase, MongoCollection
from .exceptions import CollectionException, CollectionInvalid, URIMissing, DatabaseException
from pymongo.errors import OperationFailure


class MongoFlask(object):
    def __init__(self, app=None):
        """
        # MongoFlask
        Connect a Flask application to your MongoDB client. The MongoFlask object 
        has 3 attributes: client, db, and collections. 
        1. `client` is the MongoDB instance in the computer.
        2. `db` is the Database to connect to.
        3. `collections` is a dictrionary of all the collections in the database. 
        
        To use the functions of a collection it may be done as so:
        ```python
        current_app.mongo.collections['collection'].insert_one(insert)
        ```
        or
        ```python
        mongo.collections['collection'].insert_one(insert)
        ```
        :param app: Flask application instance
        :type app: Flask

        ## Change log
        |Version|Description|
        |-------|-----------|
        |v0.01  |Initial release of API|
        |v0.02  |Changes for ease of use|
        """
        self.client = None  # MongoDB client
        self.db = None  # Application database
        self.collections = {}  # Database collections

        if app is not None:
            # App is initialized if sent as parameter else, init_app 
            # has to be called
            self.init_app(app)

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
        
        self.client = MongoConnect(uri)
        self.__database__(db_name)
        
        app.mongo = self # Create mongo attribute in Flask instance

    def __database__(self, db_name=None):
        """
        Sets the db attribute of the object.

        :param db_name: Name of the database to connect to
        :type db_name: str
        """
        if db_name is None:
            raise DatabaseException()

        self.db = MongoDatabase(self.client, db_name)
        self.collections = self.__collections__()
    
    def __collections__(self):
        """
        Retrieves Collections in DB and inserts into collections attribute. If 
        there are no collections, returns empty `dict`. Otherwise, creates a `dict`
        object with instances of the collections.
        """
        collections = self.db.list_collection_names()
        if len(collections) == 0:
            return {}
        else:
            col_dict = {}
            for collection in collections:
                col_dict[collection] = MongoCollection(self.db, collection)
            return col_dict
    
    def insert_collection(self, collection_name = None):
        """
        Inserts a new collection into the collections attribute. If collection does not
        exists, it is created.

        :param collection_name: Name of the collection to be inserted
        :param collection_name: str
        """
        if collection_name is None:
            raise CollectionException()

        try:
            self.collections[collection_name] = MongoCollection(self.db, collection_name, create=True)
        except OperationFailure:
            self.collections[collection_name] = MongoCollection(self.db, collection_name)
        return True
    
    def get_collection(self, collection_name=None) -> MongoCollection:
        """
        Retrieves a Collection instance from the collections attribute.

        :param collection_name: Name of the collection to be retrieved
        :type collection_name: str
        """
        if collection_name is None:
            raise CollectionException()

        if self.collections.get(collection_name) is None:
            raise CollectionInvalid()
        else:
            return self.collections.get(collection_name)

    def start_session(self, causal_consistency=True, default_transaction_options=None):
        return self.client.start_session(causal_consistency, default_transaction_options)
