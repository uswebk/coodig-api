from django.urls import path
from .views import RegistrationView, VerifyOtp, SendOtp, UserLoginView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('otp/verify/', VerifyOtp.as_view(), name='otp_verify'),
    path('otp/send/', SendOtp.as_view(), name='otp_send'),
]
