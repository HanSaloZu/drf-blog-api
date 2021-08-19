from .models import Ban


def ban(receiver, creator, reason=""):
    return Ban.objects.create(receiver=receiver, creator=creator,
                              reason=reason)


def unban(user):
    Ban.objects.get(receiver=user).delete()


def is_banned(user):
    return Ban.objects.all().filter(receiver=user).exists()
