from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from bans.services import check_if_user_is_banned
from utils.exceptions import Forbidden403, NotAuthenticated401


def raise_403_if_user_is_banned(user):
    if check_if_user_is_banned(user):
        raise Forbidden403(
            messages=["You are banned"],
            code="bannedUser"
        )


def raise_403_if_user_is_inactive(user):
    if not user.is_active:
        raise Forbidden403(
            messages=["Your profile is not activated"],
            code="inactiveProfile"
        )


def get_user_from_access_token_or_401(access_token):
    jwt_authenticaton = JWTAuthentication()
    validated_token = jwt_authenticaton.get_validated_token(access_token)

    try:
        return jwt_authenticaton.get_user(validated_token)
    except AuthenticationFailed:
        raise NotAuthenticated401
