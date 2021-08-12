from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import ListAPIView

from utils.views import LoginRequiredAPIView
from utils.shortcuts import raise_400_based_on_serializer
from posts.mixins import ListPostsAPIViewMixin
from posts.selectors import get_liked_posts

from .mixins import UpdateImageMixin
from .serializers import (UpdateProfileSerializer, UpdatePasswordSerailizer,
                          AuthenticatedUserProfileSerializer)


class RetrieveUpdateProfileAPIView(LoginRequiredAPIView, APIView):
    """
    Retrieves and updates the authenticated user profile
    """

    def get(self, request):
        serializer = AuthenticatedUserProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def patch(self, request):
        instance = request.user.profile
        serializer = UpdateProfileSerializer(instance, data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(AuthenticatedUserProfileSerializer(instance).data)

        raise_400_based_on_serializer(serializer)


class UpdateAvatarAPIView(LoginRequiredAPIView, UpdateImageMixin, APIView):
    """
    Updates the avatar of the authenticated user profile
    """
    image_field = "avatar"

    def get_object(self, request):
        return request.user.profile.avatar


class UpdateBannerAPIView(LoginRequiredAPIView, UpdateImageMixin, APIView):
    """
    Updates the banner of the authenticated user profile
    """
    image_field = "banner"

    def get_object(self, request):
        return request.user.profile.banner


class UpdatePasswordAPIView(LoginRequiredAPIView, APIView):
    """
    Updates the password of the authenticated user
    """

    def put(self, request):
        instance = request.user
        serializer = UpdatePasswordSerailizer(
            instance, data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)


class ListPostsAPIView(LoginRequiredAPIView, ListPostsAPIViewMixin):
    """
    Lists the posts of the authenticated user
    """

    def filter_queryset(self, queryset, kwargs):
        posts = queryset.filter(author=self.request.user)
        return super().filter_queryset(posts, kwargs)


class ListLikedPostsAPIView(LoginRequiredAPIView, ListPostsAPIViewMixin):
    """
    Lists liked posts
    """

    def get_queryset(self):
        return get_liked_posts(self.request.user)
