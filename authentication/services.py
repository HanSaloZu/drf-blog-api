from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from utils.exceptions import NotAuthenticated401


def get_user_from_access_token_or_401(access_token):
    jwt_authenticaton = JWTAuthentication()
    validated_token = jwt_authenticaton.get_validated_token(access_token)

    try:
        return jwt_authenticaton.get_user(validated_token)
    except AuthenticationFailed:
        raise NotAuthenticated401
