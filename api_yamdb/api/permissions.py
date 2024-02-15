from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrOwnerOrModeratorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # return request.method != 'POST' or request.user.is_authenticated
        return (request.method in SAFE_METHODS) or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'owner'
                or request.user.role == 'moderator'
            )# and request.method != 'PUT'
        return request.method in SAFE_METHODS



class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user.is_authenticated and request.user.role in ('owner', 'admin',))

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_authenticated:
    #         return (
    #             obj.author == request.user
    #             or request.user.role == 'admin'
    #             or request.user.role == 'owner'
    #             or request.user.role == 'moderator'
    #         )
    #     return request.method in SAFE_METHODS
