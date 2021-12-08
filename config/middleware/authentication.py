from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_user_from_request(request):
    user = get_user(request)

    if user.is_authenticated:
        return user
    try:
        user, _ = JWTAuthentication().authenticate(Request(request))
        if user is not None:
            return user
    except Exception:
        # if any exception is raised, then the user cannot be authenticated
        pass

    return user  # AnonymousUser


class AuthenticationMiddlewareJWT(MiddlewareMixin):
    """
    Authenticating JSON Web Tokens in Authorize Header
    """

    def process_request(self, request):
        user = SimpleLazyObject(lambda: get_user_user_from_request(request))
        request.user = user
