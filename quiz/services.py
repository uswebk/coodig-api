from django.db.models import Count, Subquery, Exists, OuterRef
from django.db.models.functions import Random

from account.models import Account
from quiz.models import Quiz, Tag, QuizAnswerChoice, QuizAnswer
from quiz.api.serializers import QuizAnswerSerializer, QuizChoiceSerializer


class QuizService:
    def __init__(self, quiz: Quiz):
        self.quiz = quiz

    def create_choices(self, choices: list):
        for choice in choices:
            choice['quiz_id'] = self.quiz.id
        quiz_choice_serializer = QuizChoiceSerializer(data=choices, many=True)
        quiz_choice_serializer.is_valid(raise_exception=True)
        quiz_choice_serializer.save()

    def create_tags(self, tags: list, account: Account):
        for _tag in tags:
            tag = Tag.objects.get_or_create(name=_tag['name'], defaults={'created_by': account})
            self.quiz.tags.add(tag[0])


class RandomQuizServie:
    @staticmethod
    def get_random(account: Account, limit: int):
        subquery = Subquery(
            QuizAnswer.objects.filter(quiz_id=OuterRef('pk')).filter(account_id=account.id).values('quiz_id')
        )
        return Quiz.objects.annotate(random_number=Random()).exclude(created_by=account).filter(
            is_published=True,
            choices__is_answer=True
        ).annotate(
            has_children=Exists(subquery)
        ).filter(
            has_children=False
        ).order_by('random_number')[:limit]
