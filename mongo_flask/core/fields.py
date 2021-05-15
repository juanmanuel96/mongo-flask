from .validators import validate_int, validate_str
from ..errors import ValidatorsException, ValidationError


class ErrorDetail:
    def __init__(self, **details):
        self.message = details.get('message', 'No message provided')
        details.pop('message')
        self.fix = details.get('fix', 'No fix provided')
        details.pop('fix')

        if details:  # Check if there are any details left
            for key, value in details.items():
                setattr(self, key, value)


class BaseField:
    def __init__(self, *, data=None, required=False, validators=()):
        self.required = required
        self.validators = list(validators)
        self.__data = data
        self.errors = []

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    def validate(self):
        pass

    def run_validators(self):
        for validator in self.validators:
            if not callable(validator):
                raise ValidatorsException()
            try:
                validator(self.data)
            except ValidationError as err:
                self.errors.append(ErrorDetail(**err.exception_data))


class StringField(BaseField):
    def __init__(self, *, min_length=1, max_length=255, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.validators.append(validate_str)

    def validate_length(self):
        if len(self.data) <= self.min_length or len(self.data) >= self.max_length:
            raise ValidationError(
                message=f'Length of data must be between {self.min_length} and {self.max_length}',
                fix=f'Make text no less than {self.min_length} characters or more than {self.max_length} characters'
            )


class IntegerField(BaseField):
    def __init__(self, **kwargs):
        super().__init__(validators=[validate_int], **kwargs)
        self.validators.append(validate_int)
