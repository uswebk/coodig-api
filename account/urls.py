from django.urls import path, include
from .views import TestView

urlpatterns = [
    path('', TestView.as_view()),
]
