import datetime
import hashlib
import hmac
import random

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.encoding import force_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now, timedelta
from rest_framework_simplejwt.tokens import RefreshToken

from account.consts import OTP_VALID_MINUTES, OTP_CODE_NUMBER_OF_DIGITS
from account.emails import send_reset_password
from account.exceptions import LoginError, OtpVerifyError
from account.models import Otp, Account
from coodig import settings


class LoginService:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def login(self) -> dict:
        account = authenticate(email=self.email, password=self.password)
        if account is not None:
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
            expiration_at=timezone.now() + datetime.timedelta(minutes=OTP_VALID_MINUTES),
            account_id=self.account.id
        )
        return otp

    def __get_digits(self) -> int:
        digits = ''
        for num in range(self.number_of_digits):
            digits += '9'
        return int(digits)


class OtpVerifyService:
    def __init__(self, account: Account):
        self.account = account

    def done(self, send_code: str):
        if not self.account.otps:
            raise OtpVerifyError('Invalid otp verify')
        otp = self.account.otps.last()
        if send_code != otp.code:
            raise OtpVerifyError('Wrong otp code')
        if timezone.now() > otp.expiration_at:
            raise OtpVerifyError('Expiration of validity')
        self.verify_done()

    def verify_done(self) -> None:
        self.account.email_verified_at = timezone.now()
        self.account.last_login = timezone.now()
        self.account.save()


def get_tokens_for_user(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SendResetPasswordService:
    def __init__(self, account: Account):
        self.account = account

    def execute(self) -> None:
        uid = urlsafe_base64_encode(force_bytes(self.account.id))
        token = PasswordResetTokenGenerator().make_token(self.account)
        link = settings.APP_SCHEMA + 'reset-password/' + uid + '/' + token
        expiration = now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT_SECONDS)
        payload = link + f':{expiration.timestamp()}'
        signature = hmac.new(
            key=settings.URI_SECRET_KEY.encode(),
            msg=payload.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        url = f'{link}:{expiration.timestamp()}:{signature}'

        send_reset_password(self.account.email, url)


class ResetPasswordService:
    @staticmethod
    def execute(uid: str, token: str, password: str) -> None:
        account_id = smart_str(urlsafe_base64_decode(uid))
        account = Account.objects.get(id=account_id)

        if not PasswordResetTokenGenerator().check_token(account, token):
            raise ValidationError('Token is Valid or Expired')

        account.set_password(password)
        account.save()
