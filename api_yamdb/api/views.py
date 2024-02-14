from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from content.models import Review, Title, Genre, Category
from .permissions import IsAdminOrOwnerOrModeratorOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )
    search_fields = ('name')
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    # Чтобы получить правельный набор объектов, мне нужно увидеть,
    # как будет выглядеть поле rating в классе Reviews.
    queryset = Title.objects.all()
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwnerOrModeratorOrReadOnly, ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrOwnerOrModeratorOrReadOnly, ]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_review())
