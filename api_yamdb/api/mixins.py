from rest_framework.filters import SearchFilter

from api.permissions import (IsAdminOrOwnerOrModeratorOrReadOnly,
                             IsAdminOrReadOnly)


class ReviewCommentMixin:
    permission_classes = [
        IsAdminOrOwnerOrModeratorOrReadOnly,
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
