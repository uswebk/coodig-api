from django.urls import path
from .views import RegistrationView, VerifyOtpView, SendOtpView, UserLoginView, MeView

urlpatterns = [
    path('me/', MeView.as_view(), name='account'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('otp/verify/', VerifyOtpView.as_view(), name='verify_otp'),
    path('otp/send/', SendOtpView.as_view(), name='send_otp'),
]
