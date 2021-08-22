from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions import NotFound404

from .models import Ban


def get_ban_object_by_login_or_404(login):
    try:
        return Ban.objects.get(receiver__login=login)
    except ObjectDoesNotExist:
        raise NotFound404("Invalid login or user is not banned")
