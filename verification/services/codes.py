import datetime

from django.conf import settings
from django.utils.crypto import get_random_string

from ..models import VerificationCode


def create_verification_code(user):
    verification_code = generate_verification_code()
    return VerificationCode.objects.create(user=user, code=verification_code)


def generate_verification_code():
    while True:
        code = get_random_string(
            length=6, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

        if not check_if_verification_code_exists(code):
            return code


def check_if_verification_code_exists(code):
    return VerificationCode.objects.all().filter(code=code).exists()


def verify_email_by_code(code):
    verification_code_object = VerificationCode.objects.get(code=code)
    user = verification_code_object.user

    user.is_active = True
    user.save()

    verification_code_object.delete()


def remove_expired_codes():
    code_lifetime = settings.EMAIL_VERIFICATION_CODE_LIFETIME

    VerificationCode.objects.all().filter(
        created_at__lt=datetime.datetime.now() - code_lifetime
    ).delete()
