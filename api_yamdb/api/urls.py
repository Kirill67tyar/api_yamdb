from django.urls import path, include

from accounts.views import register_user_view

app_name = 'api'

urlpatterns_v1 = [
    path('auth/signup/', register_user_view, name='signup'),
    # path('auth/token/'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
]

# http://127.0.0.1:8000/api/v1/auth/token/