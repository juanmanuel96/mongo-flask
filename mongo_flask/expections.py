from pymongo.errors import OperationFailure

class DatabaseException(Exception):
    def __init__(self, message = 'Must provide a database name'):
        super().__init__(message)

class CollectionException(Exception):
    def __init__(self, message = 'Must provide a collection name'):
        super().__init__(message)

class CollectionInvalid(Exception):
    def __init__(self, message = 'Collection does not exist'):
        super().__init__(message)

class URIMissing(Exception):
    def __init__(self, message = 'Must provide MONGO_HOST and MONGO_PORT in application config'):
        super().__init__(message)