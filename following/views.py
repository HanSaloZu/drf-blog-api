from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .service import is_following, follow_user, unfollow
from .selectors import get_user_by_id
from utils.response import APIResponse


@api_view(["GET", "POST", "DELETE"])
def follow(request, user_id):
    if not request.user.is_authenticated:
        return Response({"message": "Authorization has been denied for this request."},
                        status.HTTP_401_UNAUTHORIZED)

    response = APIResponse()
    user = request.user
    try:
        subject = get_user_by_id(user_id)
    except ObjectDoesNotExist:
        return Response({"message": "Bad request"}, status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        return Response(is_following(user, subject), status.HTTP_200_OK, content_type="application/json")

    elif request.method == "POST":
        if user_id == user.id:
            response.result_code = 1
            response.messages.append("You can't follow yourself")
            return response.complete()

        if is_following(user, subject):
            response.result_code = 1
            response.messages.append("You are already following this user")
            return response.complete()

        follow_user(user, subject)
        return response.complete()

    elif request.method == "DELETE":
        if is_following(user, subject):
            unfollow(user, subject)

            return response.complete()
        else:
            response.result_code = 1
            response.messages.append(
                "First you should follow user. Then Then you can unfollow")
            return response.complete()
