from .models import Ban


def ban_user(receiver, creator, reason=""):
    return Ban.objects.create(receiver=receiver, creator=creator,
                              reason=reason)


def unban_user(user):
    Ban.objects.get(receiver=user).delete()


def check_if_user_is_banned(user):
    return Ban.objects.all().filter(receiver=user).exists()
