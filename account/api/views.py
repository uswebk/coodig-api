from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers import AccountRegistrationSerializer, VerifyAccountSerializer, UserLoginSerializer, \
    AccountSerializer, OtpSerializer, SendPasswordResetEmailSerializer, PasswordResetSerializer
from account.emails import send_opt
from account.exceptions import OtpVerifyError, LoginError
from account.models import Account
from account.permissions import ActiveAccount
from account.services import LoginService, OtpService, OtpVerifyService, get_tokens_for_user, SendResetPasswordService, \
    ResetPasswordService


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AccountRegistrationSerializer

    def post(self, request):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            otp = OtpService().create(account)
            send_opt(otp)
        return Response({'token': get_tokens_for_user(account)}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = LoginService().login(serializer.data['email'], serializer.data['password'])
            return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
        except LoginError as e:
            return Response({'non_field_errors': ['Email or Password is not Valid']},
                            status=status.HTTP_404_NOT_FOUND)


class VerifyOtpView(APIView):
    permission_classes = [permissions.IsAuthenticated, ActiveAccount]
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        account = self.request.user
        if serializer.is_valid(raise_exception=True):
            try:
                OtpVerifyService().done(account, serializer.data['otp'])
                return Response({"messages": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"messages": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
        otp = OtpService().create(account)
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
            if account is not None:
                SendResetPasswordService().execute(account)

            return Response({'message': 'Send Reset Password Mail'}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny, ]
    serializers_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializers_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                ResetPasswordService.execute(
                    serializer.data['uid'],
                    serializer.data['token'],
                    serializer.data['password']
                )
                return Response({}, status=status.HTTP_200_OK)

            except ValidationError as e:
                return Response({'message': {e.messages[0]}}, status=status.HTTP_400_BAD_REQUEST)
