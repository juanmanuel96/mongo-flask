from ..errors import ValidationError


def validate_int(value):
    if not isinstance(value, int):
        raise ValidationError(
            message=f'Value is of type {type(value)} and should be int',
            fix='Use int values'
        )


def validate_float(value):
    if not isinstance(value, float):
        raise ValidationError(
            message=f'Value is of type {type(value)} and should be float',
            fix=f'Use float values'
        )


def validate_str(value):
    if not isinstance(value, str):
        raise ValidationError(
            message=f'Value is of type {type(value)} and should be str',
            fix='Use string values'
        )
