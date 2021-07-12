from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions import NotFound404

from .models import Profile


def get_profile_by_user_login(user_login):
    return Profile.objects.get(user__login=user_login)


def get_profile_by_user_login_or_404(user_login):
    try:
        return get_profile_by_user_login(user_login)
    except ObjectDoesNotExist:
        raise NotFound404("Invalid login, user is not found")
