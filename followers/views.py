from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from utils.views import LoginRequiredAPIView
from utils.exceptions import InvalidData400
from users.mixins import UsersListAPIViewMixin
from profiles.selectors import get_profile_by_user_login_or_404

from .selectors import get_user_followers_ids_list, get_user_followings_ids_list
from .models import FollowersModel


class FollowersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    """
    Lists the users following the authenticated user
    """

    def filter_queryset(self, queryset, kwargs):
        followers_ids = get_user_followers_ids_list(self.request.user)
        return super().filter_queryset(queryset.filter(id__in=followers_ids), kwargs)


class FollowingListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    """
    Lists the users who the authenticated user follows
    """

    def filter_queryset(self, queryset, kwargs):
        followings_ids = get_user_followings_ids_list(self.request.user)
        return super().filter_queryset(queryset.filter(id__in=followings_ids), kwargs)


class FollowingAPIView(LoginRequiredAPIView, APIView):
    """
    Check if the user is followed by the authenticated user(GET)
    Follow the specified user(PUT)
    Unfollow from the specified user(DELETE)
    """

    model = FollowersModel

    def get(self, request, login):
        target = get_profile_by_user_login_or_404(login).user
        return Response(data={"isFollowed": self.model.is_following(request.user, target)})

    def put(self, request, login):
        if login == request.user.login:
            raise InvalidData400("You can't follow yourself")

        target = get_profile_by_user_login_or_404(login).user

        if self.model.is_following(request.user, target):
            raise InvalidData400("You are already following this user")

        self.model.follow(request.user, target)
        return Response(status=HTTP_204_NO_CONTENT)

    def delete(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if self.model.is_following(request.user, target):
            self.model.unfollow(request.user, target)

        return Response(status=HTTP_204_NO_CONTENT)
