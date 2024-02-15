from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Avg
from rest_framework import permissions

from reviews.models import Review, Title, Genre, Category
from api.permissions import IsAdminOrOwnerOrModeratorOrReadOnly, IsAdminOrReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class ListCreateDestroyMixin(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyMixin):
    filter_backends = (SearchFilter,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ('name', )
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    # http_method_names = ['get', 'post', 'patch', ]


class GenreViewSet(ListCreateDestroyMixin):
    filter_backends = (SearchFilter,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    search_fields = ('name', )
    lookup_field = 'slug'


# ! ----------------------------------------------

# class GenreFilter(FilterSet):
#     slug = CharFilter()

#     class Meta:
#         model = Genre
#         fields = ['slug',]

# class TitleFilter(FilterSet):
#     genre= filters.RelatedFilter(GenreFilter, field_name='genre')

#     class Meta:
#         model = Title
#         fields = ['genre',]
#         # fields = ['slug',]


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = [
            'genre',
            'category',
            'name',
            'year',
        ]


# ! ----------------------------------------------


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', )
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete',]

    # filter_backends = (SearchFilter, TitleFilter, )
    # filterset_fields = ('genre__slug',)
    # filterset_fields = ('genre',)

    # def get_queryset(self):
    #     queryset = Title.objects.all()
    #     # Добыть параметр color из GET-запроса
    #     slug = self.request.query_params.get('slug')
    #     if slug is not None:
    #         queryset = queryset.filter(genre__slug=slug)
    #     return queryset

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAdminOrOwnerOrModeratorOrReadOnly, ]

#     def get_title(self):
#         return get_object_or_404(Title, pk=self.kwargs.get("title_id"))

#     def get_queryset(self):
#         # if self.action == 'partial_update':
#         #     self.request.user.reviews.all()
#         return self.get_title().reviews.all()

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user, title=self.get_title())



# ! ------------------------------------------------------------
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrOwnerOrModeratorOrReadOnly, ]
    http_method_names = ['get', 'post', 'patch', 'delete',]


    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get("title_id"))


    def get_queryset(self):
        return self.get_title().reviews.all()


    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrOwnerOrModeratorOrReadOnly, ]
    http_method_names = ['get', 'post', 'patch', 'delete',]

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
