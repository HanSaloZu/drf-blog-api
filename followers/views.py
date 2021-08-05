from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from utils.views import LoginRequiredAPIView
from users.mixins import UsersListAPIViewMixin
from profiles.selectors import get_profile_by_user_login_or_404

from .selectors import get_user_followers_ids_list, get_user_followings_ids_list
from .services import is_following, follow, unfollow


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

    def get(self, request, login):
        target = get_profile_by_user_login_or_404(login).user
        return Response(data={"isFollowed": is_following(request.user, target)})

    def put(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if not is_following(request.user, target):
            if login != request.user.login:
                follow(request.user, target)

        return Response(status=HTTP_204_NO_CONTENT)

    def delete(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if is_following(request.user, target):
            unfollow(request.user, target)

        return Response(status=HTTP_204_NO_CONTENT)
