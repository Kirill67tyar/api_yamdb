from django.conf import settings
from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class IsAdminOrReadOnly(BasePermission):
    """
    Всем пользователям открыт доступ только к методам "только для чтения".
    Для методов с правами на запись нужно, чтобы пользователь был
    аутентифицирован и имел роль "admin".
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or (request.user and request.user.is_authenticated and (request.user.is_admin() or request.user.is_superuser))
        

class IsAdminOrModeratorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Всем пользователям открыт доступ только к методам "только для чтения".
    Для методов с правами на запись нужно, чтобы пользователь был
    аутентифицирован и имел роль "admin" или "moderator".
    Для доступа к объекту нужно,, чтобы пользователь был
    аутентифицирован и был либо автором объекта, либо имел
    роль "admin" или "moderator".
    """

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and obj.author == request.user)
            or (request.user.is_authenticated and request.user.is_admin())
            or (request.user.is_authenticated and request.user.is_moderator)
            or (request.user.is_authenticated and request.user.is_superuser)
        )

class IsAdminOrOwner(IsAuthenticated):

    def has_permission(self, request, view):
        """
        Доступ разрушён если клиент аутентифицирован.
        Является суперюзером, или его роль admin.
        """
        return bool(request.user and request.user.is_authenticated
                    and (request.user.is_superuser or request.user.is_admin()))
