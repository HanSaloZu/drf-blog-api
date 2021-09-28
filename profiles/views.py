from django.contrib.auth import update_session_auth_hash
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from posts.mixins import ListPostsWithOrderingAPIViewMixin
from posts.selectors import get_liked_posts, get_post_by_id_or_404
from utils.shortcuts import raise_400_based_on_serializer
from utils.views import LoginRequiredAPIView

from .mixins import UpdateImageMixin
from .serializers import (AuthenticatedUserProfileSerializer,
                          UpdatePasswordSerailizer, UpdateProfileSerializer)


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
            user = serializer.save()
            update_session_auth_hash(request, user)
            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)


class ListPostsAPIView(LoginRequiredAPIView,
                       ListPostsWithOrderingAPIViewMixin):
    """
    Lists the posts of the authenticated user
    """

    def filter_queryset(self, queryset, kwargs):
        posts = queryset.filter(author=self.request.user)
        return super().filter_queryset(posts, kwargs)


class ListLikedPostsAPIView(LoginRequiredAPIView,
                            ListPostsWithOrderingAPIViewMixin):
    """
    Lists liked posts
    """

    def get_queryset(self):
        return get_liked_posts(self.request.user)


class RetrieveCreateDestroyLikedPostAPIView(LoginRequiredAPIView, APIView):
    """
    Retrieves, creates, and destroys liked post
    """

    def get(self, request, id):
        post = get_post_by_id_or_404(id)
        is_liked = request.user.like_set.all().filter(post_id=post.id).exists()

        return Response(data={
            "isLiked": is_liked
        })

    def put(self, request, id):
        post = get_post_by_id_or_404(id)
        is_liked = request.user.like_set.all().filter(post_id=post.id).exists()

        if not is_liked:
            request.user.like_set.create(post=post, user=request.user)

        return Response(data={
            "isLiked": True
        })

    def delete(self, request, id):
        post = get_post_by_id_or_404(id)
        like_object = request.user.like_set.all().filter(post_id=post.id)

        if like_object.exists():
            like_object.delete()

        return Response(data={
            "isLiked": False
        })
