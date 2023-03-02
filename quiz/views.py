from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz
from quiz.serializers import TagSerializer, QuizSerializer
from quiz.services import AnswerService, QuizService


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(created_by=user).prefetch_related('choices')

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            account = self.request.user
            data = request.data['quiz']
            data['created_by'] = account.id
            quiz_serializer = self.get_serializer(data=data)
            quiz_serializer.is_valid(raise_exception=True)
            quiz = quiz_serializer.save()

            quiz_service = QuizService(quiz)
            quiz_service.create_choices(request.data['quiz']['choices'])
            quiz_service.create_tags(request.data['tags'], account)

        return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk, created_by=self.request.user, is_deleted=False)
        quiz.is_deleted = True
        quiz.save()
        return Response({}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def answer(self, request, pk=None):
        quiz = get_object_or_404(Quiz.objects.prefetch_related('choices'), pk=pk)
        answer_service = AnswerService(quiz, self.request.user)
        answer_serializer = answer_service.create_answer(request.data['is_correct'])
        answer_service.create_answer_choices(quiz, request.data['choices'])

        return Response(answer_serializer.data, status=status.HTTP_201_CREATED)
