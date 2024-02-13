from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .permissions import IsOwnerOrReadOnly
from .serializers import (CommentsSerializer, ReviewSerializer, CategoriesSerializer, GenresSerializer,
                          TitlesWriteSerializer, TitlesReadSerializer)

from model.models import Titles, Genres, Categories


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )
    search_fields = ('name')
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    # Чтобы получить правельный набор объектов, мне нужно увидеть,
    # как будет выглядеть поле rating в классе Reviews.
    queryset = Titles.objects.all()
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer
      

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_title())


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Titles, pk=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_title())

