from django.conf import settings
from django.core.mail import send_mail
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet


def send_email_confirmation_code(confirmation_code, email):
    return send_mail(
        subject="Получение кода подтверждения",
        message=confirmation_code,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            email,
        ],
        fail_silently=True,
    )


def get_object_or_null(model, **kwargs):
    if isinstance(model, QuerySet) or isinstance(model, BaseManager):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()
