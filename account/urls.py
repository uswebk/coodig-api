from django.urls import path, include
from .views import TestView, RegistrationView

urlpatterns = [
    path('', TestView.as_view()),
    path('registar/', RegistrationView.as_view()),
]
