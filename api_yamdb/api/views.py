from rest_framework import permissions, viewsets

from model.models import Titles, Genres, Categories
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesWriteSerializer, TitlesReadSerializer)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    search_fields = ('name')
    lookup_field = 'slug'


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    # Чтобы получить правельный набор объектов, мне нужно увидеть,
    # как будет выглядеть поле rating в классе Reviews.
    queryset = Titles.objects.all()
    # Если будет свой пермишен для доступа, без токена то можно заменить
    # стандартный 'IsAuthenticatedOrReadOnly' на кастомный.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesWriteSerializer
