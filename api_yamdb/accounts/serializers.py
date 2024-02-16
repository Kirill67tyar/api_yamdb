from django.http import Http404
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    EmailField,
    CharField,
    ValidationError,
)


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

    def validate_role(self, value):
        if value == 'owner':
            raise ValidationError('Роль не может быть "owner"')
        return value

    def update(self, instance, validated_data):
        validated_data.pop('role', None)
        return super().update(instance, validated_data)


# class UserGetTokenModelSerializer(Serializer):
#     confirmation_code = CharField(
#         max_length=254,
#         required=True
#     )
#     username = CharField(
#         max_length=150,
#         required=True,
#         validators=[
#             RegexValidator(
#                 regex=r'^[\w.@+-]+$',
#                 message='Неправильный формат поля username',
#             ),
#         ],
#     )

#     def validate(self, data):
#         username = data['username']
#         confirmation_code = data['confirmation_code']
#         if not User.objects.filter(username=username).exists:
#             raise Http404('asdas')
#         if User.objects.filter(Q(username=username) & ~Q(confirmation_code=confirmation_code)).exists:
#             raise ValidationError('asdas')
#         return data

#     def validate_username(self, value):
#         if not User.objects.filter(username=value).exists:
#             raise Http404('asdas')
#         return value

# ! --------------- сериалайзер, проходят тесты --------------------
class UserGetTokenModelSerializer(ModelSerializer):
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
