from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name="genre__slug", lookup_expr="icontains")
    category = CharFilter(field_name="category__slug", lookup_expr="icontains")
    name = CharFilter(field_name="name")
    year = NumberFilter(field_name="year")

    class Meta:
        model = Title
        fields = [
            "genre",
            "category",
            "name",
            "year",
        ]
