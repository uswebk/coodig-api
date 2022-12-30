from django.urls import path, include
from .views import RegistrationView

urlpatterns = [
    path('registar/', RegistrationView.as_view()),
]
