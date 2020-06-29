from .wrappers import MongoConnect, MongoDatabase, MongoCollection
from .expections import CollectionException, OperationFailure, CollectionInvalid, URIMissing, DatabaseException

class MongoFlask(object):
    def __init__(self, app = None, db_name = None):
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
        :param db_name: Name of the database
        :type db_name: str

        ## Change log
        |Version|Description|
        |-------|-----------|
        |v0.01  |Initial release of API|
        |v0.02  |Various chnages for ease of use|
        """
        self.client = None # MongoDB client
        self.db = None # MongoDB database
        self.collections = {} # Database collections

        if app is not None:
            # App is initialized if sent as parameter else, init_app 
            # has to be called
            self.init_app(app, db_name=db_name)

    def init_app(self, app, db_name = None):
        """
        Initializes the application. Flask instance MUST have at least the 
        MONGO_HOST and MONGO_PORT in the application configuration. Username and 
        password are optional. If database name is provided, it is also initialized.

        :param app: Flask instance of the application
        :type app: Flask
        :param db_name: Name of the database to connect to
        :type db_name: str
        """
        host = app.config.get('MONGO_HOST', None)
        port = app.config.get('MONGO_PORT', None)
        username = app.config.get('MONGO_USER', None)
        pwd = app.config.get('MONGO_PWD', None)
        
        if host is None or port is None:
            raise URIMissing()
        else:
            if username is None:
                connect = f'mongodb://{host}:{port}'
            else:
                connect = f'mongodb://{username}:{pwd}@{host}:{port}'
        
        self.client = MongoConnect(connect)
        if db_name is not None:
            db_name = str(db_name)
            self.db = self.set_Database(db_name, app)
        
        app.mongo = self # Create mongo attribute in Flask instance

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

    def set_Database(self, db_name = None):
        """
        Sets the db attribute of the object.

        :param db_name: Name of the database to connect to
        :type db_name: str
        """
        if db_name is None:
            raise DatabaseException()
        else:
            self.db = MongoDatabase(self.client, db_name)
            self.collections = self.__collections__()
            return self.db
    
    def insert_Collection(self, collection_name = None):
        """
        Inserts a new collection into the collections attribute. If collection does not
        exists, it is created.

        :param collection_name: Name of the collection to be inserted
        :param collection_name: str
        """
        if collection_name is None:
            raise CollectionException()
        else:
            try:
                self.collections[collection_name] = MongoCollection(self.db, collection_name, create=True)
            except OperationFailure as failure:
                self.collections[collection_name] = MongoCollection(self.db, collection_name)
        
        return self.collections
    
    def get_collection(self, collection_name = None):
        """
        Retrieves a Collection instance from the collections attribute.

        :param collection_name: Name of the collection to be retrieved
        :type collection_name: str
        """
        if collection_name is None:
            raise CollectionException()
        else:
            if self.collections.get(collection_name) is None:
                raise CollectionInvalid()
            else:
                return self.collections.get(collection_name)