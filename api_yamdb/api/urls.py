from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.views import (
    register_user_view,
    get_token_view,
    UserModelViewSet,
)
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
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(r"users", UserModelViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", register_user_view, name="signup"),
    path(
        'v1/auth/token/',
        # TokenObtainPairView.as_view(),
        get_token_view,
        name='token_obtain_pair'
    )
]
