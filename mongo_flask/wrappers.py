from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class MongoConnect(MongoClient):
    """
    Wrapper from the pymongo.MongoClient class
    """
    def __getattr__(self, name):
        attr = super(MongoConnect, self).__getattr__(name)
        if isinstance(attr, Database):
            return MongoDatabase(self, name)
        return attr
    
    def __getitem__(self, item):
        attr = super(MongoConnect, self).__getitem__(item)
        if isinstance(attr, Database):
            return MongoDatabase(self, item)
        return attr


class MongoDatabase(Database):
    """
    Wrapper for the pymongo.database.Database class
    """
    def __getattr__(self, name):  # noqa: D105
        attr = super(MongoDatabase, self).__getattr__(name)
        if isinstance(attr, Collection):
            return MongoCollection(self, name)
        return attr

    def __getitem__(self, item):  # noqa: D105
        item_ = super(MongoDatabase, self).__getitem__(item)
        if isinstance(item_, Collection):
            return MongoCollection(self, item)
        return item_


class MongoCollection(Collection):
    """
    Wrapper class for the pymongo.collection.Collection class
    """
    def __getattr__(self, name):  # noqa: D105
        attr = super(MongoCollection, self).__getattr__(name)
        if isinstance(attr, Collection):
            db = self._Collection__database
            return MongoCollection(db, attr.name)
        return attr

    def __getitem__(self, item):  # noqa: D105
        item_ = super(MongoCollection, self).__getitem__(item)
        if isinstance(item_, Collection):
            db = self._Collection__database
            return MongoCollection(db, item_.name)
        return item_
    
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

    def find_one(self, session=None, **kwargs):
        _filter = {}.update(**kwargs)
        return super().find_one(_filter, session=session)
