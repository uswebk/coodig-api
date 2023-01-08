from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView

from quiz.models import Tag
from quiz.serializers import TagSerializer


class TagListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
