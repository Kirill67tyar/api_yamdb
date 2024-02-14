from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from accounts.serializers import UserModelSerializer
from accounts.permissions import IsAdminOrOwner

from accounts.viewsets import ListCreateModelViewSet


User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrOwner,)

    # def get_queryset(self):
    #     a = 1
    #     return User.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(
    #         user=self.request.user
    #     )


User = get_user_model()


#  Потом попытаюсь на viewset перенести, хотя возможно - нецелесообразно
@api_view(http_method_names=['POST'])
def register_user_view(request):
    dict_data = dict(request.data)
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid(raise_exception=False):
        user = serializer.save()
        send_mail(
            subject='Тема письма',
            message=user.confirmation_code,
            from_email='from@example.com',
            recipient_list=[user.email,],
            fail_silently=True,
        )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
    # if User.objects.filter(Q(email=dict_data['email'])
    #                     & Q(username=dict_data['username'])).exists():
    #     return Response(
    #         data=serializer.data,
    #         status=status.HTTP_200_OK
    #     )
    return Response(
        data=serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
