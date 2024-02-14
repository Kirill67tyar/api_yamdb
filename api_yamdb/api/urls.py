from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.views import register_user_view
from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = "api"

router_v1 = DefaultRouter()

router_v1.register(r"titles", TitleViewSet, basename="title")
router_v1.register(r"genres", GenreViewSet, basename="genre")
router_v1.register(r"categories", CategoryViewSet, basename="categorie")
router_v1.register(
    r"titles/(?P<title_id>\d+)/comments", CommentViewSet, basename="comments"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

urlpatterns_v1 = [
    path("auth/signup/", register_user_view, name="signup"),    
    path("", include(router_v1.urls)),
    # path('auth/token/'),
]
urlpatterns = [
    path("v1/", include(urlpatterns_v1)),
]
