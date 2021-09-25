from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin


def get_user_jwt(request):
    user = get_user(request)

    if user.is_authenticated:
        return user
    try:
        user, _ = JWTAuthentication().authenticate(Request(request))
        if user is not None:
            return user
    except Exception:
        pass

    return user


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    """
    Authenticating JSON Web Tokens in Authorize Header
    """

    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_jwt(request))
