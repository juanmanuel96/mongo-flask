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
