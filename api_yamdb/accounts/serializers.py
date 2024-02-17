from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.core.validators import RegexValidator
from django.db.models import Q
from django.http import Http404
from rest_framework import exceptions, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

CONFIRMATION_CODE_IS_NOT_VALID = "Код подтверждения не валиден"
EMAIL_IS_NOT_UNIQUE = "Email не уникален"
INVALID_USERNAME_FIELD_FORMAT = "Неправильный формат поля username"
NO_USER_WITH_THIS_USERNAME = "Нет пользователя с таким username"
ROLE_CANNOT_BE_OWNER = "Роль не может быть 'owner'"
THERE_IS_USER_WITH_THIS_EMAIL = (
    "Пользователь с таким email уже зарегистрирован"
)
THERE_IS_USER_WITH_THIS_USERNAME = (
    "Пользователь с таким username уже зарегистрирован"
)
USERNAME_SHOULD_NOT_HAVE_VALUE_ME = "Username не должен иметь значение 'me'"


class ExtendedUserModelSerializer(ModelSerializer):
    email = EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(), message=EMAIL_IS_NOT_UNIQUE
            )
        ],
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    def validate_role(self, value):
        if value == "owner":
            raise ValidationError(ROLE_CANNOT_BE_OWNER)
        return value

    def update(self, instance, validated_data):
        validated_data.pop("role", None)
        return super().update(instance, validated_data)


class UserGetTokenModelSerializer(Serializer):
    confirmation_code = CharField(max_length=254, required=True)
    username = CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message=INVALID_USERNAME_FIELD_FORMAT,
            ),
        ],
    )

    def validate(self, data):
        username = data["username"]
        confirmation_code = data["confirmation_code"]
        if not User.objects.filter(username=username).exists():
            raise Http404(NO_USER_WITH_THIS_USERNAME)
        if User.objects.filter(
            Q(username=username) & ~Q(confirmation_code=confirmation_code)
        ).exists():
            raise ValidationError(CONFIRMATION_CODE_IS_NOT_VALID)
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["confirmation_code"] = user.confirmation_code
        del token["password"]
        return token


class UserModelSerializer(Serializer):
    email = EmailField(max_length=254, required=True)
    username = CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message=INVALID_USERNAME_FIELD_FORMAT,
            ),
        ],
    )

    def validate_username(self, value):
        if value == "me":
            raise ValidationError(USERNAME_SHOULD_NOT_HAVE_VALUE_ME)
        return value

    def validate(self, data):
        username = data["username"]
        email = data["email"]
        if User.objects.filter(
            Q(email=email) & ~Q(username=username)
        ).exists():
            raise ValidationError(THERE_IS_USER_WITH_THIS_EMAIL)
        if User.objects.filter(
            ~Q(email=email) & Q(username=username)
        ).exists():
            raise ValidationError(THERE_IS_USER_WITH_THIS_USERNAME)
        return data


class MyTokenObtainSerializer(serializers.Serializer):
    token_class = RefreshToken
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        "no_active_account": (
            "No active account found with the given credentials"
        )
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            write_only=True)
        self.fields['confirmation_code'] = serializers.CharField(
            write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        username = authenticate_kwargs['username']
        confirmation_code = authenticate_kwargs['confirmation_code']
        if not User.objects.filter(username=username).exists():
            raise Http404(NO_USER_WITH_THIS_USERNAME)
        if User.objects.filter(
            Q(username=username) & ~Q(confirmation_code=confirmation_code)
        ).exists():
            raise ValidationError(CONFIRMATION_CODE_IS_NOT_VALID)
        self.user = get_object_or_404(
            User,
            username=username,
            confirmation_code=confirmation_code,
        )
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        refresh = self.get_token(self.user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return {'access': str(refresh.access_token)}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)
