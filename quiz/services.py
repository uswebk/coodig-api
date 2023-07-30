from django.db.models import Count, Subquery, Exists, OuterRef

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


class AnswerService:
    def __init__(self, quiz: Quiz, account: Account):
        self.quiz = quiz
        self.account = account

    def create_answer(self, is_correct: bool) -> QuizAnswerSerializer:
        answer = {
            'account_id': self.account.id,
            'quiz_id': self.quiz.id,
            'question': self.quiz.question,
            'is_correct': is_correct,
        }
        serializer = QuizAnswerSerializer(data=answer)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer

    @staticmethod
    def create_answer_choices(quiz: Quiz, choices: list) -> list:
        quiz_choices = quiz.choices.all()
        answer = quiz.answer_quiz.first()

        payload = []
        for choice in quiz_choices:
            is_select = choice.sort in choices
            payload.append(QuizAnswerChoice(
                answer_id=answer,
                choice=choice.sentence,
                is_answer=choice.is_answer,
                is_select=is_select,
            ))

        return QuizAnswerChoice.objects.bulk_create(payload)


class RandomQuizServie:
    @staticmethod
    def get_random(account: Account, limit: int):
        subquery = Subquery(
            QuizAnswer.objects.filter(quiz_id=OuterRef('pk')).filter(account_id=account.id).values('quiz_id')
        )

        return Quiz.objects.exclude(created_by=account).filter(is_published=True).annotate(
            has_children=Exists(subquery)
        ).filter(
            has_children=False
        )[:limit]
