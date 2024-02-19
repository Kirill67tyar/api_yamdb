from django.conf import settings
from django.core.mail import send_mail
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


def send_email_confirmation_code(confirmation_code, email):
    return send_mail(
        subject=settings.GETTING_CONFIRMATION_CODE,
        message=confirmation_code,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            email,
        ],
        fail_silently=True,
    )


def get_object_or_null(model, **kwargs):
    """Получает объект модели или возвращает None"""
    if isinstance(model, (QuerySet, BaseManager)):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()
