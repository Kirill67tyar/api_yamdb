from rest_framework.permissions import IsAuthenticated


class IsAdminOrOwner(IsAuthenticated):

    def has_permission(self, request, view):
        """
        Доступ разрушён если клиент аутентифицирован.
        Является суперюзером, или его роль admin или owner.
        """
        if super().has_permission(request, view):
            return bool(
                request.user.is_superuser
                or (
                    request.user.role
                    in (
                        "admin",
                        "owner",
                    )
                )
            )
        return False
