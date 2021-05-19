from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .models import FollowersModel
from utils.response import APIResponse

User = get_user_model()


class Follow(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        subject = get_object_or_404(User, id=user_id)

        return Response(FollowersModel.is_following(request.user, subject), status.HTTP_200_OK, content_type="application/json")

    def post(self, request, user_id):
        response = APIResponse()
        subject = get_object_or_404(User, id=user_id)

        if user_id == request.user.id:
            response.result_code = 1
            response.messages.append("You can't follow yourself")
            return response.complete()

        if FollowersModel.is_following(request.user, subject):
            response.result_code = 1
            response.messages.append("You are already following this user")
            return response.complete()

        FollowersModel.follow(request.user, subject)
        return response.complete()

    def delete(self, request, user_id):
        response = APIResponse()
        subject = get_object_or_404(User, id=user_id)

        if FollowersModel.is_following(request.user, subject):
            FollowersModel.unfollow(request.user, subject)

            return response.complete()
        else:
            response.result_code = 1
            response.messages.append(
                "First you should follow user. Then you can unfollow")
            return response.complete()
