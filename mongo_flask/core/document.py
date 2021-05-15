from bson import ObjectId


class Document(dict):
    def __init__(self, **kwargs):
        self.__id = ObjectId()
        super().__init__(**kwargs)

    @property
    def _id(self):
        return self.__id

    def __str__(self):
        return str(self._id)


class DocumentSet(list):
    def __str__(self):
        return str([str(doc) for doc in self])
