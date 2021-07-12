from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from utils.views import LoginRequiredAPIView
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login_or_404
from followers.selectors import get_user_followers_ids_list, get_user_followings_ids_list

from .mixins import UsersListAPIViewMixin


class UsersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    """
    Lists all users
    """
    ...


class UserFollowersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    """
    Lists the users following the specified user
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followers_ids = get_user_followers_ids_list(target_user)

        return super().filter_queryset(queryset.filter(id__in=followers_ids), kwargs)


class UserFollowingListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    """
    Lists the users who the specified user follows
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followings_ids = get_user_followings_ids_list(target_user)

        return super().filter_queryset(queryset.filter(id__in=followings_ids), kwargs)


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    """
    Retrieves the profile of the specified user
    """

    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)
