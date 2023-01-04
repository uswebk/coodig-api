from django.urls import path
from .views import RegistrationView, VerifyOtp, SendOtp

urlpatterns = [
    path('registar/', RegistrationView.as_view()),
    path('otp/verify/', VerifyOtp.as_view()),
    path('otp/send/', SendOtp.as_view()),
]
