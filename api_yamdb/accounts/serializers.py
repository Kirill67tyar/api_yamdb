from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    EmailField,
    CharField,
    ValidationError,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class UserModelSerializer(ModelSerializer):
    email = EmailField(
        max_length=254,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
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
        return data
    
    # def save(self, **kwargs):
    #     return super().save(**kwargs)    

    def is_valid(self, raise_exception=False):
        # email = self.initial_data['email']
        # username = self.initial_data['username']
        # if User.objects.filter(Q(email=email)
        #                 & Q(username=username)).exists():
        #     return True
        return super().is_valid(raise_exception)

class TokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = CharField()
        self.fields['confirmation_code'] = CharField()
        del self.fields['password']

    # def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
    #     authenticate_kwargs = {
    #         self.username_field: attrs[self.username_field],
    #         "password": attrs["password"],
    #     }
    #     try:
    #         authenticate_kwargs["request"] = self.context["request"]
    #     except KeyError:
    #         pass

    #     self.user = authenticate(**authenticate_kwargs)

    #     if not api_settings.USER_AUTHENTICATION_RULE(self.user):
    #         raise exceptions.AuthenticationFailed(
    #             self.error_messages["no_active_account"],
    #             "no_active_account",
    #         )

