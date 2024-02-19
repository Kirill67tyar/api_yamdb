from django.core.exceptions import ValidationError


USERNAME_SHOULD_NOT_HAVE_VALUE_ME = "Username не должен иметь значение 'me'"


def validate_username(value):
    if value == "me":
        raise ValidationError({'username': USERNAME_SHOULD_NOT_HAVE_VALUE_ME})
    return value
