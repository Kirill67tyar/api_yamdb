from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == "me":
        raise ValidationError(
            {'username': settings.USERNAME_SHOULD_NOT_HAVE_VALUE_ME}
        )
    return value
