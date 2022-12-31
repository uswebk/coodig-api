from django.urls import path, include
from .views import RegistrationView, AccountView, VerifyOtp

urlpatterns = [
    path('', AccountView.as_view()),
    path('registar/', RegistrationView.as_view()),
    path('otp/verify/', VerifyOtp.as_view()),
]
