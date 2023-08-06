from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, QuizViewSet, AnswerView

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('', QuizViewSet, basename='quizzes')

urlpatterns = [
    path('answers/', AnswerView.as_view(), name='quiz_answers'),
    path('', include(router.urls)),
]
