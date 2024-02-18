from rest_framework.filters import SearchFilter

from api.v1.permissions import IsAdminOrModeratorOrReadOnly, IsAdminOrReadOnly


class ReviewCommentMixin:
    permission_classes = [
        IsAdminOrModeratorOrReadOnly,
    ]
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]


class CategoryGenreMixin:
    filter_backends = (SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    search_fields = ("name",)
