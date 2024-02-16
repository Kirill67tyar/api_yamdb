from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, NumberFilter

from reviews.models import Title


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
