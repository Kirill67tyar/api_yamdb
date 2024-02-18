from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


USERNAME_SHOULD_NOT_HAVE_VALUE_ME = "Username не должен иметь значение 'me'"


def validate_username(value):
    if value == "me":
        raise ValidationError(USERNAME_SHOULD_NOT_HAVE_VALUE_ME)
    return value


@deconstructible
class MyUnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Введите валидные данные для "username". '
        'Данные должны содержать только буквы, цифры, и @/./+/-/_ символы.'
    )
    flags = 0
