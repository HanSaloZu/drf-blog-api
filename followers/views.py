from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from utils.views import LoginRequiredAPIView
from utils.exceptions import InvalidData400
from users.mixins import UsersListAPIViewMixin
from profiles.selectors import get_profile_by_user_login_or_404

from .models import FollowersModel


class FollowersListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    def filter_queryset(self, queryset, kwargs):
        followers = self.request.user.followers.only("follower_user")
        followers_ids = [i.follower_user.id for i in list(followers)]

        return super().filter_queryset(queryset.filter(id__in=followers_ids), kwargs)


class FollowingListAPIView(LoginRequiredAPIView, UsersListAPIViewMixin):
    def filter_queryset(self, queryset, kwargs):
        followings = self.request.user.following.only("following_user")
        followings_ids = [i.following_user.id for i in list(followings)]

        return super().filter_queryset(queryset.filter(id__in=followings_ids), kwargs)


class FollowingAPIView(LoginRequiredAPIView, APIView):
    model = FollowersModel

    def get(self, request, login):
        target = get_profile_by_user_login_or_404(login).user

        if self.model.is_following(request.user, target):
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_404_NOT_FOUND)

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
