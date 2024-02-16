from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db.models import Q
from django.http import Http404
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

User = get_user_model()

CONFIRMATION_CODE_IS_NOT_VALID = "Код подтверждения не валиден"
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
        validators=[UniqueValidator(queryset=User.objects.all())],
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
