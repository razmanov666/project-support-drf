from rest_framework import permissions
from userauth.models import CustomUser


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    """
    Permissopn only for Admin
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous and request.user.role == "AD":
            return True
        return False


class IsAdminOrSupport(permissions.BasePermission):
    """
    Permission for Admin or Manager
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous and request.user.role in CustomUser.MANAGERS:
            return True
        return False


class IsOwnerOrAdminOrSupport(permissions.BasePermission):
    """
    Permission for Admin, Manager or Owner of ticket
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True


class IsOwner(permissions.BasePermission):
    """
    Permission only for Owner of ticket
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
