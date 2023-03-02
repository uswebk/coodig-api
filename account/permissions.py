from rest_framework.permissions import BasePermission


class ActiveAccount(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.email_verified_at and request.user.deleted_at is None)
