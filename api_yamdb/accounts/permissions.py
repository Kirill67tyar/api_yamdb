from rest_framework.permissions import IsAuthenticated


class IsAdminOrOwner(IsAuthenticated):

    def has_permission(self, request, view):
        """
        Доступ разрушён если клиент аутентифицирован.
        Является суперюзером, или его роль admin.
        """
        return bool(request.user and request.user.is_authenticated
                    and (request.user.is_superuser or request.user.role == "admin"))
