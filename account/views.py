import datetime
import random

from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.email import send_opt
from account.exceptions import OtpVerifyError
from account.models import Account, Otp
from account.serializers import AccountRegistrationSerializer, AccountSerializer, VerifyAccountSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        token = get_tokens_for_user(account)
        otp = Otp.objects.create(
            code=str(random.randrange(0, 999999)).zfill(6),
            expiration_date=timezone.now() + datetime.timedelta(minutes=10),
            account_id=account.id
        )
        send_opt(otp)

        return Response({'token': token}, status=status.HTTP_201_CREATED)


class VerifyOtp(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            account = Account.objects.filter(
                email=email, email_verified_at__isnull=True).prefetch_related(
                Prefetch('otp_set', queryset=Otp.objects.filter(expiration_date__gte=timezone.now()).all(),
                         to_attr="otps")).first()
            try:
                if account is None:
                    raise OtpVerifyError('invalid otp verify')
                otps = account.otps
                if not otps:
                    raise OtpVerifyError('invalid otp verify')
                otp_code = serializer.data['otp']
                otp = otps[-1]
                if otp.code != otp_code:
                    raise OtpVerifyError('wrong otp code')
                account.email_verified_at = timezone.now()
                account.save()
                return Response({"message": "otp verify success"}, status=status.HTTP_200_OK)
            except OtpVerifyError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AccountView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
