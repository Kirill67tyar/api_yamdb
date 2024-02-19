
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import VALIDATE_YEAR_ERROR


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(VALIDATE_YEAR_ERROR.format(value=value, now=now))

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



