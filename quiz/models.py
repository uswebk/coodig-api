from django.db import models

from account.models import Account


class Tag(models.Model):
    class Meta:
        db_table = 'tags'

    created_by = models.ForeignKey(Account, db_column='created_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
