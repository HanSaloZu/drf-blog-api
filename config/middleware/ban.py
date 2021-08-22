from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

from bans.services import is_banned


class BanMiddleware(MiddlewareMixin):
    """
    Force banned users to log out
    """

    def process_request(self, request):
        if request.user.is_authenticated and is_banned(request.user):
            logout(request)

        return None
