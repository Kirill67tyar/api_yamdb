from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class User(AbstractUser):
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'
    OWNER_ROLE = 'owner'
    ROLE_CHOICES = (
        (USER_ROLE, 'Аутентифицированный пользователь',),
        (MODERATOR_ROLE, 'Модератор',),
        (ADMIN_ROLE, 'Администратор',),
        (OWNER_ROLE, 'Суперюзер Django ',),
    )

    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name='Выбор роли пользователя'
    )
    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='Код подтверждения'
    )

    def save(self, *args, **kwargs) -> None:
        self.password = ''
        self.confirmation_code = urlsafe_base64_encode(
            force_bytes(self.username)
        )
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('pk',)
