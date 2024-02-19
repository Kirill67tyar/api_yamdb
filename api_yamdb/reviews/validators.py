from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError(
            settings.VALIDATE_YEAR_ERROR.format(value=value, now=now)
        )
