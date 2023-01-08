from rest_framework.viewsets import ModelViewSet

from quiz.models import Tag, Quiz
from quiz.serializers import TagSerializer, QuizSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(created_by=user).prefetch_related('choices')
