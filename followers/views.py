from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.selectors import get_profile_by_user_login_or_404
from users.mixins import ListUsersAPIViewMixin
from utils.exceptions import BadRequest400, NotFound404
from utils.views import LoginRequiredAPIView

from .selectors import (get_user_followers_ids_list,
                        get_user_followings_ids_list)
from .services import follow, is_following, unfollow


class FollowersListAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users following the authenticated user
    """

    def filter_queryset(self, queryset, kwargs):
        followers_ids = get_user_followers_ids_list(self.request.user)
        queryset_of_followers = queryset.filter(id__in=followers_ids)

        return super().filter_queryset(queryset_of_followers, kwargs)


class FollowingListAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users who the authenticated user follows
    """

    def filter_queryset(self, queryset, kwargs):
        followings_ids = get_user_followings_ids_list(self.request.user)
        queryset_of_followings = queryset.filter(id__in=followings_ids)

        return super().filter_queryset(queryset_of_followings, kwargs)


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
