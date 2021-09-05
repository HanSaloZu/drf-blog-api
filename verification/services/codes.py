import datetime
from django.utils.crypto import get_random_string

from ..models import VerificationCode


def remove_expired_codes():
    VerificationCode.objects.all().filter(
        created_at__lt=datetime.datetime.now() - datetime.timedelta(minutes=15)
    ).delete()


def generate_verification_code():
    while True:
        code = get_random_string(
            length=6, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

        if not VerificationCode.objects.all().filter(code=code).exists():
            return code


def create_verification_code(user):
    remove_expired_codes()
    verification_code = generate_verification_code()
    return VerificationCode.objects.create(user=user, code=verification_code)


def verify_email_by_code(code):
    verification_code_object = VerificationCode.objects.get(code=code)
    user = verification_code_object.user

    user.is_active = True
    user.save()

    verification_code_object.delete()
    remove_expired_codes()
