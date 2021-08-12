from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from utils.views import LoginRequiredAPIView
from utils.exceptions import Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import PostSerializer, CreateUpdatePostSerializer
from .selectors import get_post_by_id_or_404
from .services import delete_post


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

        if instance.author == request.user:
            delete_post(instance)
            return Response(status=HTTP_204_NO_CONTENT)

        raise Forbidden403("You don't have permission to delete this post")
