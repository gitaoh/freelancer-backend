from rest_framework.permissions import BasePermission


class IsMasterAdmin(BasePermission):
    """
    Master-Admin have all the permissions
    User of type = 'MASTER'
    """

    def has_permission(self, request, view):
        if request.user.is_staff and request.user.is_superuser and request.user.user_type == "MASTER":
            return True
        return False


class IsMiniAdmin(BasePermission):
    """
    Mini-Admin does not have all the permissions
    User of type = 'ADMIN'
    """

    def has_permission(self, request, view):
        if request.user.is_staff and request.user.is_superuser and request.user.user_type == "ADMIN":
            return True
        return False


class IsUser(BasePermission):
    """
    IsUser - user of type = 'USER'
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == "USER")


class IsActiveUser(BasePermission):
    """
    Allow active users to login
    """

    def has_permission(self, request, view):
        return bool(request.user.is_active is True)
