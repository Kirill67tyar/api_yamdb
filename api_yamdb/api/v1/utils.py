from django.conf import settings
from django.core.mail import send_mail


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
