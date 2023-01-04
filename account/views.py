from django.db import transaction
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.email import send_opt
from account.exceptions import OtpVerifyError
from account.serializers import AccountRegistrationSerializer, VerifyAccountSerializer
from account.services import OtpService, otp_verify


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


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


class VerifyOtp(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                otp_verify(serializer.data['email'], serializer.data['otp'])
                return Response({"message": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendOtp(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        account = self.request.user
        otp_service = OtpService(account)
        otp = otp_service.create()
        send_opt(otp)

        return Response({'message': 'Send otp success'}, status=status.HTTP_200_OK)
