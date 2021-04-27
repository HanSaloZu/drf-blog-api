from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Contacts
from .services import save_photo, delete_image
from .selectors import get_profile_by_user_id, get_contacts_by_user_id
from .serializers import (ProfileSerializer, StatusSerializer,
                          UpdateProfileSerializer)
from utils.response import APIResponse
from utils.views import CustomLoginRequiredMixin


class ProfileStatusDetail(APIView):
    def get(self, request, user_id):
        try:
            profile = get_profile_by_user_id(user_id)
        except ObjectDoesNotExist:
            return Response({"message": "An error has occurred."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HttpResponse(json.dumps(profile.status), content_type="application/json")


class ProfileStatusUpdate(CustomLoginRequiredMixin, APIView):
    def put(self, request):
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


class ProfileDetail(APIView):
    def get(self, request, user_id):
        try:
            profile = get_profile_by_user_id(user_id)
        except ObjectDoesNotExist:
            return Response({"message": "An error has occurred."}, status.HTTP_500_INTERNAL_SERVER_ERROR)

        deserialized_data = ProfileSerializer(profile).data
        return Response(deserialized_data)


class ProfilePhotoUpdate(CustomLoginRequiredMixin, APIView):
    def put(self, request):
        response = APIResponse()
        image = request.data.get("image")

        if image is not None:
            profile = request.user.profile
            if profile.photo.file_id is not None:
                delete_image(profile.photo.file_id)
            link = save_photo(image, profile)
            response.data = {
                "photo": link
            }
            return response.complete()
        else:
            return Response({"message": "An error has occurred."}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileUpdate(CustomLoginRequiredMixin, APIView):
    def put(self, request):
        response = APIResponse()
        serialized_data = UpdateProfileSerializer(data=request.data)

        if serialized_data.is_valid():
            profile = request.user.profile
            data = serialized_data.data
            contacts = get_contacts_by_user_id(request.user.id)

            profile.looking_for_a_job = data["lookingForAJob"]
            profile.looking_for_a_job_description = data["LookingForAJobDescription"]
            profile.fullname = data["fullName"]
            profile.about_me = data["aboutMe"]
            data["contacts"]["main_link"] = data["contacts"].pop("mainLink")
            contacts.update(**dict(data["contacts"]))

            request.user.save()

            return response.complete()

        errors = serialized_data.errors
        for error_field in errors:
            if error_field != "contacts":
                message = errors[error_field][0]
                response.messages.append(message)
            else:
                contacts_errors = errors.get("contacts", [])
                for contact_error in contacts_errors:
                    response.messages.append(
                        f"Invalid url format (Contacts->{contact_error.capitalize()})")

        response.result_code = 1
        return response.complete()
