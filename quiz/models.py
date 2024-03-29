from django.db import models

from account.models import Account
from quiz.managers import QuizManager


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

    objects = QuizManager()

    class Meta:
        db_table = 'quizzes'


class QuizChoice(models.Model):
    quiz_id = models.ForeignKey(Quiz, related_name='choices', db_column='quiz_id', on_delete=models.CASCADE)
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


class QuizAnswer(models.Model):
    account_id = models.ForeignKey(Account, related_name='answer_account', db_column='account_id',
                                   on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, related_name='answer_quiz', db_column='quiz_id', on_delete=models.CASCADE)
    question = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_answers'


class QuizAnswerChoice(models.Model):
    answer_id = models.ForeignKey(QuizAnswer, related_name='answer_choices', db_column='answer_id',
                                  on_delete=models.CASCADE)
    choice = models.TextField()
    is_answer = models.BooleanField(default=False)
    is_select = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'quiz_answer_choices'
