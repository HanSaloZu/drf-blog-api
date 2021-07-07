from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from django.contrib.auth import get_user_model

from utils.views import LoginRequiredAPIView, ListAPIViewMixin
from utils.exceptions import InvalidData400
from users.serializers import UserSerializer
from profiles.selectors import get_profile_by_user_login_or_404

from .models import FollowersModel

User = get_user_model()


class FollowersListAPIView(LoginRequiredAPIView, ListAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        followers = self.request.user.followers.only("follower_user")
        followers_ids = [i.follower_user.id for i in list(followers)]

        return queryset.filter(
            id__in=followers_ids,
            login__contains=kwargs["q"]
        )


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
