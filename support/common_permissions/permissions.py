from rest_framework import permissions
from userauth.models import CustomUser


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsAdminOrSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in CustomUser.MANAGERS:
            return True
        return False


class IsOwnerOrAdminOrSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
