import datetime
import random

from django.db.models import Prefetch
from django.utils import timezone

from account.consts import OTP_VALID_MINUTES, OTP_CODE_NUMBER_OF_DIGITS
from account.exceptions import OtpVerifyError
from account.models import Otp, Account


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


def otp_verify(email: str, otp_code: str) -> bool:
    account = Account.objects.filter(
        email=email, email_verified_at__isnull=True).prefetch_related(
        Prefetch('otp_set', queryset=Otp.objects.filter(expiration_date__gte=timezone.now()).all(),
                 to_attr="otps")).first()
    if account is None:
        raise OtpVerifyError('invalid otp verify')
    otps = account.otps
    if not otps:
        raise OtpVerifyError('invalid otp verify')
    otp = otps[-1]
    if otp.code != otp_code:
        raise OtpVerifyError('wrong otp code')
    account.email_verified_at = timezone.now()
    account.save()

    return True
