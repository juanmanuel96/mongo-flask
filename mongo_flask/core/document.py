from bson import ObjectId


class Document(dict):
    def __init__(self, _collection, *, initial: dict = None, data: dict = None, **kwargs):
        self.__collection = _collection
        self.__id = ObjectId()
        self.initial = initial
        self.data = data
        super().__init__(**kwargs)

    @property
    def _id(self):
        return self.__id

    @property
    def collection(self):
        raise AttributeError('This attribute is read only')

    @property
    def cleaned_data(self):
        _cleaned = {}
        for key, field in self.initial:
            _cleaned[key] = field.data
        return _cleaned

    def __str__(self):
        return str(self._id)

    def save(self):
        changed_data = self.changed_data()
        if changed_data:
            # Update
            self._update(changed_data)
        else:
            # Create
            self._create()

    def delete(self):
        self.__collection.delete_one(self)

    def changed_data(self):
        """
        Returns a dictionary of the fields that changed. This is to be used for an update of the collection document.
        """
        changed_data = {}
        if not self.data:
            raise ValueError('You must provide new data')
        for key, value in self.data:
            if key not in self.initial.keys():
                raise AttributeError(f'{self.__class__} does not have attr of name {key}')
            if value != self.cleaned_data[key]:
                changed_data[key] = value
        return changed_data

    def _update(self, update_data):
        self.__collection.update_one({'_id': self._id}, update=update_data)

    def _create(self):
        self.__collection.insert_one(**self.cleaned_data)


class DocumentSet(list):
    def __str__(self):
        return str([str(doc) for doc in self])
