from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
        if not email:
            raise ValueError('User must have and email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user


class Account(AbstractBaseUser):
    class Meta:
        db_table = 'accounts'

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email_verified_at = models.DateTimeField(null=True, )
    deleted_at = models.DateTimeField(null=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


class Otp(models.Model):
    class Meta:
        db_table = 'account_otps'

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
