from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models

from users.validators import validate_username
from django.contrib.auth.validators import UnicodeUsernameValidator

class User(AbstractUser):
    ROLE_CHOICES = (
        (settings.USER_ROLE, 'Аутентифицированный пользователь',),
        (settings.MODERATOR_ROLE, 'Модератор',),
        (settings.ADMIN_ROLE, 'Администратор',),
    )
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        'username',
        max_length=settings.MAX_LENGTH_USERNAME,
        unique=True,
        help_text=f'Обязательное. Символов <= {settings.MAX_LENGTH_USERNAME}',
        validators=[username_validator, validate_username, ],
        error_messages={
            'уникальность': settings.THERE_IS_USER_WITH_THIS_USERNAME,
        },
    )
    email = models.EmailField('емэйл', blank=False, unique=True)
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=settings.MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=settings.USER_ROLE,
        verbose_name='Выбор роли пользователя'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    @property
    def is_moderator(self):
        return self.role == settings.MODERATOR_ROLE

    
    @property
    def superuser(self):
        return self.role == settings.ADMIN_ROLE or self.is_superuser

    class Meta:
        ordering = ('username', '-date_joined',)

    def __str__(self):
        return f'таааа-шааа - {self.email}'
    