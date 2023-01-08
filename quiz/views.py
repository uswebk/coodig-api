from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz
from quiz.serializers import TagSerializer, QuizSerializer


class TagListView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.prefetch_related('choices')
    serializer_class = QuizSerializer
