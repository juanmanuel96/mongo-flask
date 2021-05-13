from bson import ObjectId
from .wrappers import MongoCollection
from .document import Document
from .fields import BaseField
from ..errors import MissingFieldsException, CollectionException


class BaseFields(list):
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
    __client__session__ = None
    collection_name = None
    __id = ObjectId()

    def __init__(self, database, collection_name, **kwargs):
        if not self.collection_name:
            raise CollectionException()
        super().__init__(database, self.collection_name, **kwargs)
        self.base_fields = self.__set_base_fields__()
        self.errors = list()

    def __set_base_fields__(self):
        base_fields = BaseFields()
        non_dunder = [simple for simple in dir(self) if not simple.startswith('__') and not simple.startswith('_')]

        for name in non_dunder:
            class_attr = getattr(self, name)
            if not callable(class_attr) and isinstance(class_attr, BaseField):
                base_fields.append({name: getattr(self, name)})

        if not base_fields:
            raise MissingFieldsException(self)

        return base_fields

    def __str__(self):
        return self.__class__

    # @property
    # def collection_name(self):
    #     return self.__collection_name

    def list_find(self, *args, **kwargs):
        """
        Returns a list of the pymongo cursor
        """
        cursor = super().find(*args, **kwargs)
        return list(cursor)

    def find_limit(self, limit, *args, **kwargs):
        """
        Returns a list of the first docs found. The amount returned will be set
        by `limit`.

        :param limit: The number of the first documents to retrieved from the entire collection
        :type limit: int
        """
        int(limit)
        cursor = super().find(*args, **kwargs)
        total = [next(cursor) for _ in range(limit)]
        return total

    def all(self):
        return super().find()

    def filter(self, **kwargs):
        return super().find(**kwargs)

    def _get(self, **document):
        pass

    def get(self, **kwargs) -> Document:
        _filter = {}.update(**kwargs)
        with self.__client__session__() as session:
            _document = super().find_one(_filter, session=session)
        document = self._set_document_fields(**_document)
        return document

    def _save(self):
        pass

    def save(self):
        pass

    def _set_document_fields(self, **_document) -> Document:
        _doc = {}
        for field in self.base_fields:
            name = field.keys()[0]
            field_class = field.values()[0]
            document_field = field_class(data=_document.get(name))
            _doc.update({name: document_field})
        return Document(**_doc)

    @property
    def is_valid(self):
        return not self.errors


class CollectionModel(BaseCollection):
    pass
