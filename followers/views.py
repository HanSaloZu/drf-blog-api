from rest_framework.views import APIView
from rest_framework.response import Response

from utils.views import LoginRequiredAPIView
from utils.exceptions import NotFound404, BadRequest400
from users.mixins import ListUsersAPIViewMixin
from profiles.selectors import get_profile_by_user_login_or_404

from .selectors import (get_user_followers_ids_list,
                        get_user_followings_ids_list)
from .services import is_following, follow, unfollow


class FollowersListAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users following the authenticated user
    """

    def filter_queryset(self, queryset, kwargs):
        followers_ids = get_user_followers_ids_list(self.request.user)
        return super().filter_queryset(
            queryset.filter(id__in=followers_ids),
            kwargs
        )


class FollowingListAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users who the authenticated user follows
    """

    def filter_queryset(self, queryset, kwargs):
        followings_ids = get_user_followings_ids_list(self.request.user)
        return super().filter_queryset(
            queryset.filter(id__in=followings_ids),
            kwargs
        )


class FollowingAPIView(LoginRequiredAPIView, APIView):
    """
    Check if the user is followed by the authenticated user(GET)
    Follow the specified user(PUT)
    Unfollow from the specified user(DELETE)
    """

    def get(self, request, login):
        target = get_profile_by_user_login_or_404(login).user
        return Response(data={
            "isFollowed": is_following(request.user, target)
        })

    def put(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if login == request.user.login:
            raise BadRequest400("You cannot follow yourself")

        if not is_following(request.user, target):
            follow(request.user, target)

        return Response(data={
            "isFollowed": is_following(request.user, target)
        })

    def delete(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if not is_following(request.user, target):
            raise NotFound404("You are not yet followed this user")

        unfollow(request.user, target)

        return Response(data={
            "isFollowed": is_following(request.user, target)
        })
