from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from followers.selectors import (get_user_followers_ids_list,
                                 get_user_followings_ids_list)
from posts.mixins import ListPostsWithOrderingAPIViewMixin
from profiles.selectors import get_profile_by_user_login_or_404
from profiles.serializers import ProfileSerializer
from utils.exceptions import Forbidden403, NotAuthenticated401
from utils.shortcuts import raise_400_based_on_serializer
from utils.views import LoginRequiredAPIView
from verification.services.codes import create_verification_code
from verification.services.email import send_verification_email

from .mixins import ListUsersAPIViewMixin
from .serializers import CreateUserSerializer


class ListCreateUsersAPIView(ListUsersAPIViewMixin):
    """
    Lists all users or creates one
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise NotAuthenticated401
        return super().get(request, *args, **kwargs)

    def post(self, request):
        if request.user.is_authenticated:
            raise Forbidden403("You are already authenticated")

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            verification_code = create_verification_code(user).code
            send_verification_email(user, verification_code)

            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)


class ListUserFollowersAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users following the specified user
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followers_ids = get_user_followers_ids_list(target_user)
        queryset_of_followers = queryset.filter(id__in=followers_ids)

        return super().filter_queryset(queryset_of_followers, kwargs)


class ListUserFollowingAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users who the specified user follows
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followings_ids = get_user_followings_ids_list(target_user)
        queryset_of_followings = queryset.filter(id__in=followings_ids)

        return super().filter_queryset(queryset_of_followings, kwargs)


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    """
    Retrieves the profile of the specified user
    """

    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)


class ListUserPostsAPIView(LoginRequiredAPIView,
                           ListPostsWithOrderingAPIViewMixin):
    """
    Lists the posts of the specified user
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        posts = queryset.filter(author=target_user)

        return super().filter_queryset(posts, kwargs)
