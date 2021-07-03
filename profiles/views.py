from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.core.files import File

from utils.response import APIResponse
from utils.views import LoginRequiredAPIView
from utils.responses import InvalidData400Response
from utils.shortcuts import generate_messages_list_by_serializer_errors

from .services.photos import update_photo
from .serializers import (UpdateProfileSerializer, ProfileSerializer,
                          ProfilePreferencesSerializer)


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


class UpdatePhotoAPIView(LoginRequiredAPIView, APIView):
    def put(self, request):
        image = request.data.get("image")

        if isinstance(image, File):
            instance = request.user.profile.photo
            link = update_photo(instance, image)

            return Response({"photo": link})

        return InvalidData400Response(
            messages=["File not provided"],
            fields_errors={"image": "File not provided"}
        ).complete()


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
