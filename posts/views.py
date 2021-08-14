from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from utils.views import LoginRequiredAPIView
from utils.exceptions import Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import PostSerializer, CreateUpdatePostSerializer
from .selectors import get_post_by_id_or_404
from .services import delete_post
from .mixins import ListPostsAPIViewMixin


class ListCreatePostAPIView(LoginRequiredAPIView, ListPostsAPIViewMixin):
    """
    Lists all posts or creates one
    """

    def post(self, request):
        serializer = CreateUpdatePostSerializer(
            data=request.data, context={"request": request})

        if serializer.is_valid():
            post = serializer.save()

            return Response(
                data=self.serializer_class(post, context={
                    "request": request
                }).data,
                status=HTTP_201_CREATED,
                headers={
                    "Location": reverse("post", kwargs={"id": post.id})
                }
            )

        raise_400_based_on_serializer(serializer)


class RetrieveUpdateDestroyPostAPIView(LoginRequiredAPIView, APIView):
    """
    Retrieves, updates, or deletes the specified post
    """

    def get(self, request, id):
        instance = get_post_by_id_or_404(id)

        return Response(PostSerializer(
            instance=instance, context={"request": request}
        ).data)

    def patch(self, request, id):
        instance = get_post_by_id_or_404(id)

        if instance.author != request.user:
            raise Forbidden403("You don't have permission to edit this post")

        serializer = CreateUpdatePostSerializer(
            instance, request.data, partial=True)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(PostSerializer(
                instance,
                context={"request": request}
            ).data)

        raise_400_based_on_serializer(serializer)

    def delete(self, request, id):
        instance = get_post_by_id_or_404(id)

        if instance.author == request.user or request.user.is_staff:
            delete_post(instance)
            return Response(status=HTTP_204_NO_CONTENT)

        raise Forbidden403("You don't have permission to delete this post")
