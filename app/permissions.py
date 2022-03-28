from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUser(BasePermission):
    """Check if user is superuser"""
    message = 'You must be superuser'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrReadOnly(BasePermission):
    """Check if user is superuser or read only"""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_superuser
        )


class IsSuperUserOrAuthor(BasePermission):
    """Check if user is superuser or author"""
    message = 'You must be superuser or author'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.is_superuser
            or request.user.is_authenticated and request.user.is_author
        )


class IsSuperUserOrAuthorOrReadOnly(BasePermission):
    """Check if user is superuser or author or read only"""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user.is_authenticated and request.user.is_superuser
            or request.user.is_authenticated and obj.author == request.user
        )
