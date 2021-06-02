from bson import ObjectId
from .wrappers import MongoCollection
from .document import Document, DocumentSet
from .fields import BaseField
from ..errors import MissingFieldsException, CollectionException


class CollectionFields(list):
    __data = dict()

    def __init__(self, **kwargs):
        super().__init__()
        if kwargs:
            self.__data.update(**kwargs)

    def append(self, __object: dict) -> None:
        if not isinstance(__object, dict):
            raise Exception('append object must be dict')
        super().append(__object)
        self.__data.update(**__object)

    @property
    def data(self):
        return self.__data

    @property
    def keys(self):
        return self.__data.keys()

    def __str__(self):
        return self.__data.keys()


class BaseCollection(MongoCollection):
    __client_session__ = None
    collection_name = None
    __id = ObjectId()

    def __init__(self, database, **kwargs):
        if not self.collection_name:
            raise CollectionException()
        super().__init__(database, self.collection_name, **kwargs)
        self.base_fields = self.__set_base_fields__()
        self.errors = list()

    def __set_base_fields__(self):
        base_fields = CollectionFields()
        non_dunder = [simp for simp in dir(self) if not simp.startswith('__') and not simp.startswith('_')]

        for name in non_dunder:
            class_attr = getattr(self, name)
            if not callable(class_attr) and isinstance(class_attr, BaseField):
                base_fields.append({name: getattr(self, name)})

        if not base_fields:
            raise MissingFieldsException(self)

        return base_fields

    def __str__(self):
        return self.__class__

    @property
    def client_session(self):
        return self.__client_session__

    @client_session.setter
    def client_session(self, value):
        self.__client_session__ = value

    @property
    def is_valid(self, raise_exep=False):
        if raise_exep:
            if self.errors:
                raise Exception('Not Valid')
        else:
            return not self.errors

    def _set_document_fields(self, **_document) -> Document:
        _doc = {}
        for field in self.base_fields:
            name = list(field.keys())[0]
            field_class = list(field.values())[0]
            field_class.data = _document.get(name)  # Set the data of the field
            _doc.update({name: field_class})
        return Document(self, **_doc)

    ##########
    # Collection operations
    ##########
    def find_limit(self, limit, *args, **kwargs) -> DocumentSet:
        """
        Returns a list of the first docs found. The amount returned will be set
        by `limit`.

        :param limit: The number of the first documents to retrieved from the entire collection
        :type limit: int
        """
        docu_set = DocumentSet()
        int(limit)
        _filter = {}
        if kwargs:
            _filter = dict(**kwargs)
        cursor = super().find(*args, _filter)
        for idx, document in enumerate(cursor):
            _document = self._set_document_fields(**document)
            docu_set.append(_document)
            if idx + 1 == limit:
                break
        return docu_set

    def all(self) -> DocumentSet:
        docu_set = DocumentSet()
        cursor = super().find()
        for document in cursor:
            _document = self._set_document_fields(**document)
            docu_set.append(_document)
        return docu_set

    def filter(self, **kwargs) -> DocumentSet:
        docu_set = DocumentSet()
        _filter = dict(**kwargs)
        cursor = super().find(_filter)
        for document in cursor:
            _document = self._set_document_fields(**document)
            docu_set.append(_document)
        return docu_set

    def get(self, **kwargs) -> Document:
        _filter = dict(**kwargs)
        _document = super().find_one(_filter)
        data = _document if _document else {}
        document = self._set_document_fields(**data)
        return document

    # TODO: Override method to return the created document object
    def insert_one(self, session=None, **kwargs):
        _document = dict(**kwargs)
        return super().insert_one(document=_document, session=session)

    # TODO: Override method to return the updated document object
    def update_one(self, document: Document, update: dict, **kwargs):
        _update = {'$set': update}
        return super().update_one({'_id': str(document)}, _update, **kwargs)

    def delete_one(self, document: Document, **kwargs):
        kwargs = self._remove_session(**kwargs)
        return super().delete_one({'_id': str(document)}, **kwargs)

    def multiple_operation(self, pipeline=()):
        """
        WIP
        This method allows the user to create a multiple operation sequence of queries. The sequence is established
        by the pipeline. The pipeline should be a tuple of dictionaries where the key is the method (i.e. insert_one)
        and the value are the parameters of the method.

        Here is the structure for each valid method:
        1) insert_one
            {'insert_one': {'field': 'value'}}
        2) update_one
            {'update_one': {
                'doc': document,
                'set' : {'my_field': 'my_value'}
                }
            }
        3) delete_one
            {'delete_one' : document}

        How the pipeline is constructed is entirely up to the user, but the structure of the pipeline methods must
        follow the above guidelines.

        :param pipeline: Sequence of methods to run
        :type pipeline: tuple
        """
        valid_operations = ('insert_one', 'update_one', 'delete_one')
        self._validate_pipeline(pipeline, valid_operations)
        with self.client_session() as session:
            with session.start_transaction():
                try:
                    for operation in pipeline:
                        method = list(operation.keys())[0]
                        params = list(operation.values())
                        if method == 'update_one':
                            op = getattr(self, method)
                            op(document=params[0]['doc'], update=params[1]['set'], session=session)
                        if method == 'insert_one':
                            op = getattr(self, method)
                            op(**params[0], session=session)
                        if method == 'delete_one':
                            op = getattr(self, method)
                            op(document=params[0], session=session)
                except Exception as err:  # If ANY error occurs, stop operation and end transaction
                    session.abort_transaction()
                    session.end_session()
            session.commit_transaction()  # Commit the transaction
            session.end_session()  # End the session
        return session.has_ended()  # Return if the session has ended

    def _validate_pipeline(self, pipeline: tuple, operations=()):
        for method in pipeline:
            if not isinstance(method, dict):
                raise ValueError('Pipeline must be a list of dictionaries')
            if method.keys() not in operations:
                raise ValueError(f'Only the following are valid operations: {operations}')
            if not isinstance(method.values(), dict):
                raise ValueError('Method values must be dictionary')
            if method == 'update_one':
                if not isinstance(method['update_one'], dict):
                    raise ValueError('update_one method must be a dictionary with filter and update data')
                if not isinstance(method['update_one'].get('filter'), Document):
                    raise ValueError('Filter must be of type Document')
                if not isinstance(method['update_one'].get('set'), dict):
                    raise ValueError('update_one set value must be of type dictionary')


class CollectionModel(BaseCollection):
    pass
