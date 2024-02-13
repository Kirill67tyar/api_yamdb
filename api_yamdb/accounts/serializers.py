from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, EmailField


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
