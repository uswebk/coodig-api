import datetime
import random

from django.utils import timezone

from account.consts import OTP_VALID_MINUTES, OTP_CODE_NUMBER_OF_DIGITS
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
