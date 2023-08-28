from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, QuizViewSet, AnswerViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('answers', AnswerViewSet, basename='answers')
router.register('', QuizViewSet, basename='quizzes')

urlpatterns = [
    path('', include(router.urls)),
]
