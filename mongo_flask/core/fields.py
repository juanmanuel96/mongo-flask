from .validators import validate_int
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
    def __init__(self, *, required=False, validators=()):
        self.required = required
        self.validators = validators
        self.data = None
        self.errors = []

    def validate(self):
        for validator in self.validators:
            if not callable(validator):
                raise ValidatorsException()
            try:
                validator(self.data)
            except ValidationError as err:
                self.errors.append(ErrorDetail(**err.exception_data))


class StringField(BaseField):
    def __init__(self, *, min_length=None, max_length=None, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length

    def __validate_lengths__(self):
        if len(self.data) <= self.min_length or len(self.data) >= self.max_length:
            raise ValidationError(
                message=f'Length of data must be between {self.min_length} and {self.max_length}',
                fix=f'Make text no less than {self.min_length} characters or more than {self.max_length} characters'
            )


class IntegerField(BaseField):
    def __init__(self, **kwargs):
        extra_validators = []
        if kwargs.get('validators'):
            extra_validators += kwargs['validators']
            kwargs.pop('validators')

        super().__init__(validators=[validate_int])
        if extra_validators:
            self.validators += extra_validators
