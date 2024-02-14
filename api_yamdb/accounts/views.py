from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination

from accounts.serializers import UserModelSerializer, ExtendedUserModelSerializer, UserGetTokenModelSerializer
from accounts.permissions import IsAdminOrOwner



User = get_user_model()


class UserModelViewSet(ModelViewSet):
    serializer_class = ExtendedUserModelSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrOwner,)
    # lookup_field = 'username'
    # # lookup_url_kwarg = 'username'
    # lookup_url_kwarg = r'^[\w.@+-]+\Z'
#     r'posts/(?P<post_id>\d+)/comments',

  
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
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid(raise_exception=False):
        user = serializer.save()
        # username = serializer.validated_data['username']
        # email = serializer.validated_data['email']
        # if User.objects.filter(Q(email=email)
        #                     & Q(username=username)).exists():
        #     return Response(
        #         data=serializer.data,
        #         status=status.HTTP_200_OK
        #     )
        # user = User.objects.create(
        #     username=username,
        #     email=email,
        # )
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
    # return Response(
    #     data=serializer.data,
    #     status=status.HTTP_200_OK
    # )
    return Response(
        data=serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



class TokenObtainPairWithConfirmationView(TokenObtainPairView):
    @staticmethod
    @api_view(['POST'])
    def obtain_confirmation_token(request):
        username = request.data.get('username', None)
        confirmation_code = request.data.get('confirmation_code', None)

        if username and confirmation_code:
            # Провести проверку confirmation_code
            # Например, сравнить его с сохраненным значением в базе данных
            user = get_object_or_404(
                    User,
                    username=username,
                    confirmation_code=confirmation_code,
                )
            # Если confirmation_code верен, создать и вернуть JWT-токен
            refresh = RefreshToken.for_user(user)  # Предполагается, что вы найдете пользователя по username
            access_token = str(refresh.access_token)

            return Response({'access': access_token}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username or confirmation_code'}, status=status.HTTP_400_BAD_REQUEST)



def generate_token(user):
    token = Token.objects.update_or_create(user=user)
    return TokenObtainSerializer(instance=token).data

@api_view(http_method_names=['POST'])
def authenticate_user_view(request):

    serializer = UserGetTokenModelSerializer(data=request.data)
    if serializer.is_valid(raise_exception=False):
        data = serializer.data
        user = get_object_or_404(
            User,
            username=data['username'],
            confirmation_code=data['confirmation_code'],
        )
        token = generate_token(user)
        response_data = {
            'access': token['access_token']
        }
        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )
    return Response(
        data=serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
    



