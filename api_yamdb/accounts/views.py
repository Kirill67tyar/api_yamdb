from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import UserModelSerializer


"""
send_mail(
    subject='Тема письма',          
    message='Текст сообщения',  
    from_email='from@example.com',
    recipient_list=['to@example.com'],
    fail_silently=True,
) 
"""

User = get_user_model()


#  Потом попытаюсь на viewset перенести, хотя возможно - нецелесообразно
@api_view(http_method_names=['POST'])
def register_user_view(request):
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
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
    return Response(
        data=serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
