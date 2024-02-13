from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


app_name = 'api

router = routers.DefaultRouter()
router.register(r'titles', TitlesViewSet, basename='title')
router.register(r'genres', GenresViewSet, basename='genre')
router.register(r'categories', CategoriesViewSet, basename='categorie')


urlpatterns = [
    path('', include(router.urls)),
]
