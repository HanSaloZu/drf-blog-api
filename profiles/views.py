from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files import File

from utils.views import LoginRequiredAPIView
from utils.responses import InvalidData400Response
from utils.shortcuts import generate_messages_list_by_serializer_errors

from .services.photos import update_photo
from .serializers import (UpdateProfileSerializer, ProfileSerializer,
                          PreferencesSerializer)


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


class RetrieveUpdatePreferencesAPIView(LoginRequiredAPIView, APIView):
    def get(self, request):
        serializer = PreferencesSerializer(request.user.profile.preferences)
        return Response(serializer.data)

    def put(self, request):
        instance = request.user.profile.preferences
        serializer = PreferencesSerializer(instance, data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(PreferencesSerializer(instance).data)

        errors = serializer.errors
        messages = generate_messages_list_by_serializer_errors(errors)

        return InvalidData400Response(
            messages=messages,
            fields_errors=errors
        ).complete()
