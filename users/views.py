from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from utils.views import LoginRequiredAPIView
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login_or_404

from .mixins import UsersListAPIViewMixin


class UsersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    ...


class UserFollowersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followers = target_user.followers.only("follower_user")
        followers_ids = [i.follower_user.id for i in list(followers)]

        return super().filter_queryset(queryset.filter(id__in=followers_ids), kwargs)


class UserFollowingListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followings = target_user.following.only("following_user")
        followings_ids = [i.following_user.id for i in list(followings)]

        return super().filter_queryset(queryset.filter(id__in=followings_ids), kwargs)


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)
