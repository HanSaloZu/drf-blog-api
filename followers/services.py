from .models import Follower


def is_following(user, target):
    obj = Follower.objects.filter(follower_user=user, following_user=target)
    return obj.exists()


def follow(user, target):
    obj = Follower.objects.create(follower_user=user, following_user=target)
    obj.save()

    return obj


def unfollow(user, target):
    Follower.objects.filter(follower_user=user,
                            following_user=target).delete()
