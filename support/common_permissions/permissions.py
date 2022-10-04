from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to non-authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsOwnerOrAdminOrSupport(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.user == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
