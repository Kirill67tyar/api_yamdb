from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.validators import MyUnicodeUsernameValidator, validate_username


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
            'Обязательное. Символов <= 150'),
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

    def save(self, *args, **kwargs) -> None:
        default_token_generator.make_token(self)
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
