import datetime
import random

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.email import send_opt
from account.models import Account, Otp
from account.serializers import AccountRegistrationSerializer, AccountSerializer


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


class AccountView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
