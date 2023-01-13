from account.models import Account
from quiz.models import Quiz, QuizAnswer
from quiz.serializers import QuizAnswerSerializer


class AnswerService:
    def __init__(self, quiz: Quiz, account: Account):
        self.quiz = quiz
        self.account = account

    def create_answer(self, is_correct: bool):
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
