from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .selectors import get_user_by_id
from .models import FollowersModel
from utils.response import APIResponse
from utils.views import CustomLoginRequiredMixin


class Follow(CustomLoginRequiredMixin, APIView):
    model = FollowersModel

    def get(self, request, user_id):
        try:
            subject = get_user_by_id(user_id)
        except ObjectDoesNotExist:
            return Response({"message": "Bad request"}, status.HTTP_400_BAD_REQUEST)

        return Response(self.model.is_following(request.user, subject), status.HTTP_200_OK, content_type="application/json")

    def post(self, request, user_id):
        response = APIResponse()
        subject = get_user_by_id(user_id)

        if user_id == request.user.id:
            response.result_code = 1
            response.messages.append("You can't follow yourself")
            return response.complete()

        if self.model.is_following(request.user, subject):
            response.result_code = 1
            response.messages.append("You are already following this user")
            return response.complete()

        self.model.follow(request.user, subject)
        return response.complete()

    def delete(self, request, user_id):
        response = APIResponse()
        subject = get_user_by_id(user_id)

        if self.model.is_following(request.user, subject):
            self.model.unfollow(request.user, subject)

            return response.complete()
        else:
            response.result_code = 1
            response.messages.append(
                "First you should follow user. Then you can unfollow")
            return response.complete()
