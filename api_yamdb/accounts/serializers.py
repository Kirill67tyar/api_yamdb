from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    EmailField,
    CharField,
    ValidationError,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions

User = get_user_model()


class ExtendedUserModelSerializer(ModelSerializer):
    email = EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        # read_only_fields = ('role',)

    def validate_role(self, value):
        if value == 'owner':
            raise ValidationError('blablalba')
        return value
    
    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)

        # validators = [
        #     UniqueValidator(
        #         queryset=User.objects.all(),
        #         fields=('email', ),
        #         # message=(
        #         #     'Ошибка: вы уже подписаны на пользователя'
        #         #     'доступного по ключу "following".'
        #         #     'Нельзя подписываться дважды.'
        #         # )
        #     ),
        # ]


class UserGetTokenModelSerializer(ModelSerializer):

    # username = CharField(
    #     max_length=150,
    #     required=True)
    # confirmation_code = CharField(
    #     max_length=254,
    #     required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class UserModelSerializer(Serializer):
    email = EmailField(
        max_length=254,
        required=True
    )
    username = CharField(
        max_length=150,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Неправильный формат поля username',
            ),
        ],
    )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('username не должен иметь значение "me"')
        return value

    def validate(self, data):
        username = data['username']
        email = data['email']
        if User.objects.filter(Q(email=email) & ~Q(username=username)).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        if User.objects.filter(~Q(email=email) & Q(username=username)).exists():
            raise ValidationError(
                'Пользователь с таким username уже зарегистрирован'
            )
        return data

    # def save(self, **kwargs):
    #     return super().save(**kwargs)

    # def is_valid(self, raise_exception=False):
    #     # result = super().is_valid(raise_exception)
    #     # email = self.initial_data['email']
    #     # username = self.initial_data['username']
    #     # if User.objects.filter(Q(email=email)
    #     #                 & Q(username=username)).exists():
    #     #     return True
    #     # return result
    #     return super().is_valid(raise_exception)
