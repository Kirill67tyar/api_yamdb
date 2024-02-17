from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import IsAdminOrOwner
from accounts.serializers import (ExtendedUserModelSerializer,
                                  UserSerializer, UserGetTokenSerializer)
from accounts.utils import send_email_confirmation_code, get_object_or_null


User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = ExtendedUserModelSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    permission_classes = (IsAdminOrOwner,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
        elif request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.validated_data.pop("role", None)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
def register_user_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.create()
    return Response(data=data, status=status.HTTP_200_OK)


from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(http_method_names=["POST"])
def get_token_view(request):
    serializer = UserGetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()
    refresh = RefreshToken.for_user(user)
    data = {'token': str(refresh.access_token)}
    return Response(data=data, status=status.HTTP_200_OK)
