from account.models import Account
from quiz.models import Quiz, Tag
from quiz.serializers import QuizAnswerSerializer, QuizChoiceSerializer


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
