import datetime
import os
import random

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.mail import EmailMessage

from account.models import Account, Otp
from account.serializers import AccountRegistrationSerializer, AccountSerializer, OtpSerializer


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

        # TODO:Email Service
        body = 'OPT: ' + otp.code
        data = {
            'subject': 'Reset Your Password',
            'body': body,
            'to_email': account.email
        }

        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()

        return Response({'token': token}, status=status.HTTP_201_CREATED)


class AccountView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
