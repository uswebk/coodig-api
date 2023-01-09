from django.db import models

from account.models import Account


class Tag(models.Model):
    created_by = models.ForeignKey(Account, db_column='created_by', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tags'


class Quiz(models.Model):
    created_by = models.ForeignKey(Account, db_column='created_by', on_delete=models.CASCADE)
    question = models.TextField()
    is_published = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='QuizTag', blank=True)

    class Meta:
        db_table = 'quizzes'


class QuizChoice(models.Model):
    quiz_id = models.ForeignKey(Quiz, related_name='choices', on_delete=models.CASCADE)
    sentence = models.TextField()
    is_answer = models.BooleanField(default=False)
    sort = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_choices'


class QuizTag(models.Model):
    quiz_id = models.ForeignKey(Quiz, related_name='quiz', db_column='quiz_id', on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, related_name='tag', db_column='tag_id', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quizzes_tags'
