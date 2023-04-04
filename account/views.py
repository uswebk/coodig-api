from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import force_bytes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.emails import send_opt, send_reset_password
from account.exceptions import OtpVerifyError, LoginError
from account.models import Account
from account.permissions import ActiveAccount
from account.serializers import AccountRegistrationSerializer, VerifyAccountSerializer, UserLoginSerializer, \
    AccountSerializer, OtpSerializer, SendPasswordResetEmailSerializer
from account.services import LoginService, OtpService, OtpVerifyService, get_tokens_for_user, SendResetPasswordService

from django.utils.http import urlsafe_base64_encode

from coodig import settings


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AccountRegistrationSerializer

    def post(self, request):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            otp_service = OtpService(account)
            otp = otp_service.create()
            send_opt(otp)
        return Response({'token': get_tokens_for_user(account)}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            login_service = LoginService(serializer.data['email'], serializer.data['password'])
            token = login_service.login()
            return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
        except LoginError as e:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class VerifyOtpView(APIView):
    permission_classes = [permissions.IsAuthenticated, ActiveAccount]
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        account = self.request.user
        if serializer.is_valid(raise_exception=True):
            try:
                otp_verify_service = OtpVerifyService(account)
                otp_verify_service.done(serializer.data['otp'])
                return Response({"message": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OtpView(APIView):
    permission_classes = [permissions.IsAuthenticated, ActiveAccount]
    serializer_class = OtpSerializer

    def get(self, request):
        account = self.request.user
        otps = account.otps
        if otps is None:
            return Response({'message': 'Not Found Otp'}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.serializer_class(otps.last()).data, status=status.HTTP_200_OK)


class SendOtpView(APIView):
    permission_classes = [permissions.IsAuthenticated, ActiveAccount]

    def post(self, request):
        account = self.request.user
        otp_service = OtpService(account)
        otp = otp_service.create()
        send_opt(otp)
        return Response({'message': 'Send otp success'}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated, ActiveAccount]

    def get(self, request):
        account = self.request.user
        return Response(AccountSerializer(instance=account).data, status=status.HTTP_200_OK)


class SendResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = SendPasswordResetEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            account = Account.objects.filter(email=serializer.data['email']).first()
            if account is None:
                return Response({'message': 'Send Reset Password Mail Fail'}, status=status.HTTP_404_NOT_FOUND)
            SendResetPasswordService(account).execute()

            return Response({'message': 'Send Reset Password Mail'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        # STEP1. request uid & token & password serializer
        # STEP2. set password
        return Response({}, status=status.HTTP_200_OK)
