from bson import ObjectId
from .wrappers import MongoCollection
# from ..errors import


class BaseCollection(MongoCollection):
    __client__session__ = None
    __collection_name = ''
    __id = ObjectId()

    def __init__(self, database, collection_name, **kwargs):
        self.__collection_name = collection_name
        super().__init__(database, collection_name, **kwargs)
        self.base_fields = self.__set_base_fields__()
        self.errors = list()

    def __set_base_fields__(self):
        base_fields = []
        for _ in dir(self):
            if not _.startswith('__') and not callable(getattr(self, _)) and not isinstance(getattr(self, _), None):
                base_fields.append(_)

        if not base_fields:
            raise Exception('Missing fields')  # No defined fields Exception
        if '_id' in base_fields:
            delattr(self, '_id')
            idx = base_fields.index('_id')
            base_fields.pop(idx)
        return base_fields

    @property
    def collection_name(self):
        return self.__collection_name

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

    def fetch(self, **kwargs):
        return super().find(**kwargs)

    def get(self, **kwargs):
        _filter = {}.update(**kwargs)
        with self.__client__session__() as session:
            document = super().find_one(_filter, session=session)
        return self

    def _get(self, **document):
        pass

    def save(self):
        pass

    def _save(self):
        pass

    @property
    def is_valid(self):
        return not self.errors
