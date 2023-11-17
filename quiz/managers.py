from django.db import models
from django.db.models import Subquery, Exists, OuterRef
from django.db.models.functions import Random


class QuizQuerySet(models.QuerySet):
    pass


class QuizManager(models.Manager.from_queryset(QuizQuerySet)):
    pass
