from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from api.filters import TitleFilter
from api.mixins import CategoryGenreMixin, ReviewCommentMixin
from api.permissions import IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from api.viewsets import ListCreateDestroyModelViewSet
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(CategoryGenreMixin, ListCreateDestroyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin, ListCreateDestroyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    filter_backends = (
        SearchFilter,
        DjangoFilterBackend,
    )
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)
    queryset = (
        Title.objects.order_by("pk").annotate(rating=Avg("reviews__score"))
    )
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
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
