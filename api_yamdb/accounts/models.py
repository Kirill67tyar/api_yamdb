from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.tokens import default_token_generator
from accounts.validators import MyUnicodeUsernameValidator, validate_username

"""
from django.contrib.auth.tokens import default_token_generator

token = default_token_generator.make_token(user)  # c2jupz-5eb9d1f18edb9d7d8d8d52136953400f
default_token_generator.check_token(user, token)  # True
"""


class User(AbstractUser):
    ROLE_CHOICES = (
        (settings.USER_ROLE, 'Аутентифицированный пользователь',),
        (settings.MODERATOR_ROLE, 'Модератор',),
        (settings.ADMIN_ROLE, 'Администратор',),
    )
    username_validator = MyUnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_username,],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=25,
        choices=ROLE_CHOICES,
        default=settings.USER_ROLE,
        verbose_name='Выбор роли пользователя'
    )
    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='Код подтверждения'
    )

    def save(self, *args, **kwargs) -> None:
        self.confirmation_code = urlsafe_base64_encode(
            force_bytes(self.username)
        )
        # token = default_token_generator.make_token(self)
        # default_token_generator.make_token(self)
        return super().save(*args, **kwargs)

    def is_user(self):
        return self.role == 'user'

    def is_moderator(self):
        return self.role == 'moderator'

    def is_admin(self):
        return self.role == 'admin'

    @property
    def superuser(self):
        return self.role == 'admin' and self.is_superuser

    class Meta:
        ordering = ('username', '-date_joined',)
