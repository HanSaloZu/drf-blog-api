from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.generics import RetrieveAPIView
from django.urls import reverse

from authentication.serializers import RegistrationSerializer
from utils.views import LoginRequiredAPIView
from utils.exceptions import Forbidden403
from utils.shortcuts import raise_400_based_on_serializer
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login_or_404
from followers.selectors import (get_user_followers_ids_list,
                                 get_user_followings_ids_list)
from posts.mixins import ListPostsAPIViewMixin

from .mixins import ListUsersAPIViewMixin


class ListCreateUsersAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists all users or creates one
    """

    def post(self, request):
        if not request.user.is_staff:
            raise Forbidden403(
                "You don't have permission to access this resource")

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()

            return Response(
                data=ProfileSerializer(user.profile).data,
                status=HTTP_201_CREATED,
                headers={"Location": reverse(
                    "user_profile_detail", kwargs={"login": user.login})}
            )

        raise_400_based_on_serializer(serializer)


class ListUserFollowersAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users following the specified user
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followers_ids = get_user_followers_ids_list(target_user)

        return super().filter_queryset(
            queryset.filter(id__in=followers_ids), kwargs
        )


class ListUserFollowingAPIView(LoginRequiredAPIView, ListUsersAPIViewMixin):
    """
    Lists the users who the specified user follows
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        followings_ids = get_user_followings_ids_list(target_user)

        return super().filter_queryset(
            queryset.filter(id__in=followings_ids), kwargs
        )


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    """
    Retrieves the profile of the specified user
    """

    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)


class ListUserPostsAPIView(LoginRequiredAPIView, ListPostsAPIViewMixin):
    """
    Lists the posts of the specified user
    """

    def filter_queryset(self, queryset, kwargs):
        target_user = get_profile_by_user_login_or_404(kwargs["login"]).user
        posts = queryset.filter(author=target_user)

        return super().filter_queryset(posts, kwargs)
