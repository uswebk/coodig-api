from django.db import transaction
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.email import send_opt
from account.exceptions import OtpVerifyError
from account.models import Account
from account.serializers import AccountRegistrationSerializer, AccountSerializer, VerifyAccountSerializer
from account.services import OtpService, otp_verify


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        with transaction.atomic():
            serializer = AccountRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            otp_service = OtpService(account)
            otp = otp_service.create()
        send_opt(otp)

        return Response({'token': get_tokens_for_user(account)}, status=status.HTTP_201_CREATED)


class VerifyOtp(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                otp_verify(serializer.data['email'], serializer.data['otp'])
                return Response({"message": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccountView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
