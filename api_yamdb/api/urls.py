from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet, CategoriesViewSet, GenresViewSet, TitlesViewSet

from accounts.views import register_user_view

app_name = 'api


router = DefaultRouter()

router.register(r'titles', TitlesViewSet, basename='title')
router.register(r'genres', GenresViewSet, basename='genre')
router.register(r'categories', CategoriesViewSet, basename='categorie')

router.register(
    r'titles/(?P<title_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)

urlpatterns_v1 = [
    path('auth/signup/', register_user_view, name='signup'),
    # path('auth/token/'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1))
    path('v1/', include(router.urls)),
]

# http://127.0.0.1:8000/api/v1/auth/token/
