from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import json

from .selectors import get_profile_by_user_id
from utils.response import APIResponse
from .serializers import PhotosExtendedProfileSerializer, StatusSerializer, PhotosSerializer


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
    deserialized_data = PhotosExtendedProfileSerializer(profile).data
    photos = deserialized_data["photos"]

    if photos["small"] and photos["large"]:
        host = request.scheme + "://" + request.get_host()
        photos["small"] = host + photos["small"]
        photos["large"] = host + photos["large"]

    return Response(deserialized_data)


@api_view(["PUT"])
def profile_photo_update(request):
    if not request.user.is_authenticated:
        return Response({"message": "Authorization has been denied for this request."},
                        status.HTTP_401_UNAUTHORIZED)

    response = APIResponse()
    data = {
        "small": request.data.get("image"),
        "large": request.data.get("image")
    }
    serialized_data = PhotosSerializer(
        request.user.profile.photos, data=data)

    if serialized_data.is_valid():
        photos = serialized_data.save()
        host = request.scheme + "://" + request.get_host()
        response.data = {
            "photos": {
                "small": host + photos.small.url,
                "large": host + photos.large.url
            }
        }

        return response.complete()
    elif serialized_data.errors and serialized_data.errors:
        response.result_code = 1
        response.messages.append(serialized_data.errors["small"][0])
        return response.complete()
