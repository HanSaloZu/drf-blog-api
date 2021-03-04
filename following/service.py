from .models import FollowersModel


def is_following(user, subject):
    pair = FollowersModel.objects.filter(
        follower_user=user, following_user=subject)
    return pair.exists()


def follow_user(user, subject):
    FollowersModel.objects.create(
        follower_user=user, following_user=subject).save()


def unfollow(user, subject):
    FollowersModel.objects.filter(
        follower_user=user, following_user=subject).delete()
