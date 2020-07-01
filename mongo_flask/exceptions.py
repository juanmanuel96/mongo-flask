class PyVersionInvalid(Exception):
    def __init__(self, message = 'Python version must be 3 or higher'):
        super.__init__(message)

class URIMissing(Exception):
    def __init__(self, message = 'Must provide at least MONGO_HOST and MONGO_PORT in application config'):
        super().__init__(message)

class DatabaseException(Exception):
    def __init__(self, message = 'Must provide a MONGO_DATABASE configuration variable'):
        super().__init__(message)

class CollectionException(Exception):
    def __init__(self, message = 'Must provide a collection name'):
        super().__init__(message)

class CollectionInvalid(Exception):
    def __init__(self, message = 'Collection does not exist'):
        super().__init__(message)

class MissingAmount(Exception):
    def __init__(self, message = 'Must provide an amount'):
        super().__init__(message)