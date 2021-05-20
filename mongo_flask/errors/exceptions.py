class BaseMongoException(Exception):
    status_code = 0
    message = ''
    fix = ''

    def __init__(self, message=None, fix=None) -> None:
        if message:
            self.message = message
        if fix:
            self.fix = fix
        super().__init__(self.construct_error_message)

    def __str__(self):
        return self.construct_error_message

    @property
    def construct_error_message(self) -> str:
        message = f"""
        Error Code: {self.status_code}
        Message: {self.message}
        Fix: {self.fix}
        """
        return message

    @property
    def exception_data(self) -> dict:
        return {
            'message': self.message,
            'fix': self.fix
        }


class PyVersionInvalid(BaseMongoException):
    status_code = 1
    message = 'Python version is not equal or greater than 3'
    fix = 'Upgrade your Python version to 3 or higher'


class URIMissing(BaseMongoException):
    status_code = 2
    message = 'MONGO_HOST and MONGO_PORT are required in configuration'
    fix = 'Include MONGO_HOST and MONGO_PORT in configuration'


class DatabaseException(BaseMongoException):
    status_code = 3
    message = 'MONGO_DATABASE environment variable missing'
    fix = 'Add MONGO_DATABASE variable to your environment variable or configuration file'


class CollectionException(BaseMongoException):
    status_code = 4
    message = 'Collection name attribute cannot be empty str or None'
    fix = 'Add collection name to class'


class CollectionInvalid(BaseMongoException):
    status_code = 5
    message = 'Collection does not exist'
    fix = 'Create collection on database or invoke MongoFlask register_collection method'


class ValidationError(BaseMongoException):
    status_code = 6
    message = 'The field value is not valid'
    fix = 'Provide a valid value'


class ValidatorsException(BaseMongoException):
    status_code = 7
    message = 'This validator is not a callable function'
    fix = 'Validators must be a list of functions'


class MissingFieldsException(BaseMongoException):
    status_code = 8
    message = '{collection} class is missing fields'
    fix = 'Add fields to {collection} class'

    def __init__(self, collection_cls=None):
        if collection_cls:
            self.message.format(collection=collection_cls)
            self.fix.format(collection=collection_cls)
        else:
            self.message.format(collection='Collection')
            self.fix.format(collection='Collection')
        super().__init__()


class InvalidClass(BaseMongoException):
    status_code = 9
    message = '{invalid_class} is not a valid class'
    fix = 'Create a class that inherits from CollectionModel'

    def __init__(self, invalid_class):
        self.message.format(invalid_class=invalid_class.__class__)


class RegistrationException(BaseMongoException):
    status_code = 10
    message = 'Unable to register collection'
    fix = 'Try again later'
