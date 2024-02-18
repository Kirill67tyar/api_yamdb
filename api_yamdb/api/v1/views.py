from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.filters import TitleFilter
from api.v1.mixins import CategoryGenreMixin, ReviewCommentMixin
from api.v1.permissions import IsAdminOrOwner, IsAdminOrReadOnly
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                ExtendedUserModelSerializer, GenreSerializer,
                                ReviewSerializer, TitleReadSerializer,
                                TitleWriteSerializer, UserGetTokenSerializer,
                                UserSerializer)
from api.v1.viewsets import ListCreateDestroyModelViewSet
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CategoryViewSet(CategoryGenreMixin, ListCreateDestroyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin, ListCreateDestroyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.order_by("pk").annotate(rating=Avg("reviews__score"))
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (
        SearchFilter,
        DjangoFilterBackend,
    )
    search_fields = ("name",)
    filterset_class = TitleFilter
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ReviewCommentMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ReviewCommentMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get("title_id"),
            pk=self.kwargs.get("review_id")
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


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


@api_view(http_method_names=["POST"])
def get_token_view(request):
    serializer = UserGetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.get_user()
    refresh = RefreshToken.for_user(user)
    data = {'token': str(refresh.access_token)}
    return Response(data=data, status=status.HTTP_200_OK)
