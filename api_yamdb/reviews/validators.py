from django.core.exceptions import ValidationError
from django.utils import timezone

from api_yamdb.settings import VALIDATE_YEAR_ERROR


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(VALIDATE_YEAR_ERROR.format(value=value, now=now))
