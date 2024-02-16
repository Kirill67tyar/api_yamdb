from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerOrModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return bool(
                obj.author == request.user
                or request.user.role in ('admin', 'owner', 'moderator',)
            )  # and request.method != 'PUT'
        return request.method in SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role in ('owner', 'admin',))
        )
