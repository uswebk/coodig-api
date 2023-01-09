from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from account.emails import send_opt
from account.exceptions import OtpVerifyError, LoginError
from account.serializers import AccountRegistrationSerializer, VerifyAccountSerializer, UserLoginSerializer
from account.services import LoginService, OtpService, OtpVerifyService, get_tokens_for_user


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
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                otp_verify_service = OtpVerifyService(serializer.data['email'])
                account = otp_verify_service.get_account()
                if account is None or not account.otps:
                    raise OtpVerifyError('invalid otp verify')
                otp = account.otps[-1]
                if otp.code != serializer.data['otp']:
                    raise OtpVerifyError('wrong otp code')
                otp_verify_service.otp_verify_done()
                return Response({"message": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendOtpView(APIView):

    def post(self, request):
        account = self.request.user
        otp_service = OtpService(account)
        otp = otp_service.create()
        send_opt(otp)
        return Response({'message': 'Send otp success'}, status=status.HTTP_200_OK)
