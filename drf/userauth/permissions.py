from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)
