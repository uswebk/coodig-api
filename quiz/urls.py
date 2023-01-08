from django.urls import path, include
from rest_framework import routers

from .views import TagListView, QuizViewSet

router = routers.DefaultRouter()
router.register('', QuizViewSet, basename='quizzes')

urlpatterns = [
    path('tags/', TagListView.as_view(), name='tag_list'),
    path('', include(router.urls)),
]
