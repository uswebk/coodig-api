from django.urls import path, include
from .views import RegistrationView, AccountView

urlpatterns = [
    path('', AccountView.as_view()),
    path('registar/', RegistrationView.as_view()),
]
