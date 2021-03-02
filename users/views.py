from rest_framework.decorators import api_view

from .serializers import UserSerializer
from utils.response import APIResponse


@api_view(["GET"])
def user_detail(request, format=None):  # auth/me
    user = request.user
    response = APIResponse()

    if user.is_anonymous:
        response.result_code = 1
        response.messages.append("You are not authorized")
        return response.complete()

    response.data = UserSerializer(user).data
    return response.complete()
