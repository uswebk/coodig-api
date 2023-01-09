from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz
from quiz.serializers import TagSerializer, QuizSerializer, QuizChoiceSerializer


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
            quiz_serializer = QuizSerializer(data=request.data['quiz'])
            quiz_serializer.is_valid(raise_exception=True)
            quiz = quiz_serializer.save()

            choices = request.data['quiz']['choices']
            for choice in choices:
                choice['quiz_id'] = quiz.id
            quiz_choice_serializer = QuizChoiceSerializer(data=choices, many=True)
            quiz_choice_serializer.is_valid(raise_exception=True)
            quiz_choice_serializer.save()

            tags = request.data['tags']
            for _tag in tags:
                tag = Tag.objects.get_or_create(name=_tag['name'], defaults={'created_by': request.user})
                quiz.tags.add(tag[0])
        return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)
