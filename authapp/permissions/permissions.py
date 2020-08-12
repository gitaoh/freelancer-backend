from rest_framework.permissions import BasePermission


class IsMasterAdmin(BasePermission):
    """
    Master-Admin have all the permissions
    User of type = 'MASTER'
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == "MASTER")


class IsMiniAdmin(BasePermission):
    """
    Mini-Admin does not have all the permissions
    User of type = 'ADMIN'
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == "ADMIN")


class IsUser(BasePermission):
    """
    IsUser - user of type = 'USER'
    """

    def has_permission(self, request, view):
        return bool(request.user.user_type == "USER")
