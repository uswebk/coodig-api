import datetime
import random

from django.contrib.auth import authenticate
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from account.consts import OTP_VALID_MINUTES, OTP_CODE_NUMBER_OF_DIGITS
from account.exceptions import LoginError
from account.models import Otp, Account


class LoginService:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def login(self) -> dict:
        account = authenticate(email=self.email, password=self.password)
        if account is not None:
            if account.email_verified_at is None:
                raise LoginError()
            account.last_login = timezone.now()
            account.save()
            return get_tokens_for_user(account)
        else:
            raise LoginError()


class OtpService:
    def __init__(self, account: Account):
        self.account = account
        self.number_of_digits = OTP_CODE_NUMBER_OF_DIGITS

    def create(self) -> Otp:
        digits = self.__get_digits()
        otp = Otp.objects.create(
            code=str(random.randrange(0, digits)).zfill(self.number_of_digits),
            expiration_date=timezone.now() + datetime.timedelta(minutes=OTP_VALID_MINUTES),
            account_id=self.account.id
        )
        return otp

    def __get_digits(self) -> int:
        digits = ''
        for num in range(self.number_of_digits):
            digits += '9'
        return int(digits)


class OtpVerifyService:
    def __init__(self, email: str):
        self.account = Account.objects.filter(
            email=email, email_verified_at__isnull=True).prefetch_related(
            Prefetch('otp_set', queryset=Otp.objects.filter(expiration_date__gte=timezone.now()).all(),
                     to_attr="otps")).first()

    def get_account(self):
        return self.account

    def otp_verify_done(self) -> None:
        self.account.email_verified_at = timezone.now()
        self.account.save()


def get_tokens_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
