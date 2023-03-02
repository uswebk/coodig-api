import os

from django.core.mail import EmailMessage


def send_mail(subject, body, to):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=os.environ.get('EMAIL_FROM'),
        to=to
    )
    email.send()


def send_opt(otp):
    subject = 'OTP Verify'
    body = 'Enter the code within 10 minutes \n OTP: ' + otp.code
    to_email = otp.account.email

    send_mail(subject, body, [to_email])
