from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .services import save_photo, delete_image
from .serializers import (UpdateProfileSerializer, ProfileSerializer,
                          ProfilePreferencesSerializer)
from utils.response import APIResponse
from utils.views import LoginRequiredAPIView
from utils.responses import InvalidData400Response
from utils.shortcuts import generate_messages_list_by_serializer_errors


class RetrieveUpdateProfileAPIView(LoginRequiredAPIView, APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def patch(self, request):
        instance = request.user.profile
        serializer = UpdateProfileSerializer(
            instance, data=request.data, partial=True)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(ProfileSerializer(instance).data)

        errors = serializer.errors
        messages = generate_messages_list_by_serializer_errors(errors)

        return InvalidData400Response(
            messages=messages,
            fields_errors=errors
        ).complete()


class ProfilePhotoUpdate(APIView):
    permission_classes = [IsAuthenticated]

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


class ProfilePreferences(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfilePreferencesSerializer

    def get_object(self):
        return self.request.user.profile.preferences

    def put(self, request):
        response = APIResponse()
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            request.user.profile.preferences.theme = serialized_data.data["theme"]
            request.user.save()
            return response.complete()

        response.result_code = 1
        errors = serialized_data.errors
        for error_field in errors:
            message = errors[error_field][0]
            response.messages.append(message)
            response.fields_errors.append({
                "field": error_field,
                "error": message
            })
        return response.complete()
