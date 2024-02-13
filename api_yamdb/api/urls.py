from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


app_name = 'api

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet, basename='title')
router.register(r'genres', GenresViewSet, basename='genre')
router.register(r'categories', CategoriesViewSet, basename='categorie')

from accounts.views import register_user_view


urlpatterns_v1 = [
    path('auth/signup/', register_user_view, name='signup'),
    # path('auth/token/'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
    path('', include(router.urls)),
]

# http://127.0.0.1:8000/api/v1/auth/token/