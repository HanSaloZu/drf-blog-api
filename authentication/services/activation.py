from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

from ..tokens import confirmation_token


User = get_user_model()


def generate_uidb64(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def generate_profile_activation_url(token, uidb64):
    url_parts = list(urlparse(settings.EMAIL_CONFIRMATION_URL))
    query = dict(parse_qsl(url_parts[4]))
    query.update({"token": token, "uidb64": uidb64})
    url_parts[4] = urlencode(query)

    return urlunparse(url_parts)


def get_user_by_uidb64_or_none(uidb64):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    return user


def activate_user_profile(credentials):
    user = get_user_by_uidb64_or_none(credentials["uidb64"])

    if user is not None and confirmation_token.check_token(user, credentials["token"]):
        user.is_active = True
        user.save()

    return user
