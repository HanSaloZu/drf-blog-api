from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json

from .selectors import get_profile_by_user_id
from utils.response import APIResponse
from .serializers import PhotosExtendedProfileSerializer, StatusSerializer


@api_view(["GET"])
def profile_status_detail(request, user_id):
    profile = get_profile_by_user_id(user_id)

    return HttpResponse(json.dumps(profile.status), content_type="application/json")


@api_view(["PUT"])
def profile_status_update(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authorization has been denied for this request."},
                        status.HTTP_401_UNAUTHORIZED)

    serialized_data = StatusSerializer(data=request.data)
    response = APIResponse()

    if serialized_data.is_valid():
        user = request.user
        user.profile.status = serialized_data.data["status"]
        user.save()

        return response.complete()
    elif serialized_data.errors["status"][0].code == "max_length":
        response = APIResponse()
        response.result_code = 1
        response.messages.append(serialized_data.errors["status"][0])

        return response.complete()

    return Response({"message": "An error has occurred."}, status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def profile_detail(request, user_id):
    profile = get_profile_by_user_id(user_id)
    return Response(PhotosExtendedProfileSerializer(profile).data)
