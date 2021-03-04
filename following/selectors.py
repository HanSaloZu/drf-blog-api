from django.contrib.auth import get_user_model

from .models import FollowersModel

User = get_user_model()


def get_user_by_id(id):
    return User.objects.get(id=id)


def get_all_user_followings(user):
    return FollowersModel.objects.filter(follower_user=user).only("following_user")
