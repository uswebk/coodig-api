from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


class ActiveAccount(BasePermission):

    def __init__(self):
        self.user_model = get_user_model()

    def has_permission(self, request, view):
        return self.user is not None and self.user.email_verified_at and self.user.deleted_at is None
