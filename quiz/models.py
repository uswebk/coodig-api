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


class Quiz(models.Model):
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True)

    class Meta:
        db_table = 'quizzes'

    created_by = models.ForeignKey(Account, db_column='created_by', on_delete=models.CASCADE)
    question = models.TextField()
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuizChoice(models.Model):
    class Meta:
        db_table = 'quiz_choices'

    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    sentence = models.TextField()
    is_answer = models.BooleanField(default=False)
    sort = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
