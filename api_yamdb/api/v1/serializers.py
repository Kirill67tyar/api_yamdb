from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        Serializer, ValidationError)
from rest_framework.validators import UniqueValidator

from api.v1.utils import get_object_or_null, send_email_confirmation_code
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username


User = get_user_model()

# ! -=-=-=- неиспользуемые константы -=-=-=-
NO_USER_WITH_THIS_USERNAME = "Нет пользователя с таким username"
ROLE_CANNOT_BE_OWNER = "Роль не может быть 'owner'"
USERNAME_SHOULD_NOT_HAVE_VALUE_ME = "Username не должен иметь значение 'me'"
# ! -=-=-=- неиспользуемые константы -=-=-=-


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ("id",)
        model = Category
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ("id",)
        model = Genre
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="slug"
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )

    def to_representation(self, title):
        return TitleReadSerializer(title).data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ("title",)

    def validate(self, data):
        user = self.context["request"].user
        title_id = self.context["view"].kwargs.get("title_id")
        if self.context["request"].method == 'POST':
            if user.reviews.filter(title=title_id).exists():
                raise serializers.ValidationError(settings.ERROR_BAD_REQUEST)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        exclude = ("review",)


class ExtendedUserModelSerializer(ModelSerializer):
    email = EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(), message=settings.EMAIL_IS_NOT_UNIQUE
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
    


class UserSerializer(Serializer):
    email = EmailField(max_length=settings.MAX_LENGTH_EMAIL, required=True)
    username = CharField(
        max_length=150,
        required=True,
        validators=[
            UnicodeUsernameValidator(
                message=settings.INVALID_USERNAME_FIELD_FORMAT),
            validate_username
        ],
    )

    def validate(self, data):
        username = data["username"]
        email = data["email"]
        if User.objects.filter(
            Q(email=email) & ~Q(username=username)
        ).exists():
            raise ValidationError(settings.THERE_IS_USER_WITH_THIS_EMAIL)
        if User.objects.filter(
            ~Q(email=email) & Q(username=username)
        ).exists():
            raise ValidationError(settings.THERE_IS_USER_WITH_THIS_USERNAME)
        return data

    def create(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        user = get_object_or_null(
            User,
            username=username,
            email=email
        )
        if user:
            confirmation_code = default_token_generator.make_token(user)
            send_email_confirmation_code(
                confirmation_code=confirmation_code,
                email=user.email,
            )
            return self.validated_data
        user = User.objects.create(
            username=username,
            email=email,
        )
        confirmation_code = default_token_generator.make_token(user)
        send_email_confirmation_code(
            confirmation_code=confirmation_code,
            email=user.email,
        )
        return self.validated_data


class UserGetTokenSerializer(Serializer):
    confirmation_code = CharField(max_length=settings.MAX_LENGTH_EMAIL, required=True)
    username = CharField(
        max_length=150,
        required=True,
        validators=[
            UnicodeUsernameValidator(
                message=settings.USERNAME_IS_NOT_UNIQUE),
            validate_username
        ],
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user, data['confirmation_code']):
            raise ValidationError(settings.CONFIRMATION_CODE_IS_NOT_VALID)
        return data

    def get_user(self):
        username = self.validated_data['username']
        return get_object_or_404(
            User,
            username=username,
        )
