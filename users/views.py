from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model

from utils.views import LoginRequiredAPIView, ListAPIViewMixin
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login_or_404

from .serializers import UserSerializer

User = get_user_model()


class UsersListAPIView(LoginRequiredAPIView, ListAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(login__contains=kwargs["q"])


class UserFollowersListAPIView(LoginRequiredAPIView, ListAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followers = target_user.followers.only("follower_user")
        followers_ids = [i.follower_user.id for i in list(followers)]

        return queryset.filter(
            id__in=followers_ids,
            login__contains=kwargs["q"]
        )


class UserFollowingListAPIView(LoginRequiredAPIView, ListAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followings = target_user.following.only("following_user")
        followings_ids = [i.following_user.id for i in list(followings)]

        return queryset.filter(
            id__in=followings_ids,
            login__contains=kwargs["q"]
        )


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)
