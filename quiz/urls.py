from django.urls import path, include
from rest_framework import routers

from .views import TagViewSet, QuizReadOnlyViewSet

router = routers.DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('', QuizReadOnlyViewSet, basename='quizzes')

urlpatterns = [
    path('', include(router.urls)),
]
