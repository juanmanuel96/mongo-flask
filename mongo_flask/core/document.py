from bson import ObjectId


class Document:
    __id = ObjectId()

    def __init__(self, **kwargs):
        if kwargs:
            for name, field in kwargs.items():
                setattr(self, name, field)

    @property
    def _id(self):
        return self.__id

    def __str__(self):
        return str(self._id)


class DocumentSet(list):
    def __str__(self):
        return str([str(doc) for doc in self])
