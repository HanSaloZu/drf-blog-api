from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.core.files import File

from utils.views import LoginRequiredAPIView
from utils.responses import InvalidData400Response
from utils.shortcuts import generate_messages_list_by_serializer_errors

from .services.photos import update_photo
from .serializers import (UpdateProfileSerializer, ProfileSerializer,
                          PreferencesSerializer, UpdatePasswordSerailizer)


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


class UpdatePasswordAPIView(LoginRequiredAPIView, APIView):
    def put(self, request):
        instance = request.user
        serializer = UpdatePasswordSerailizer(
            instance, data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)

        errors = serializer.errors
        return InvalidData400Response(
            messages=generate_messages_list_by_serializer_errors(errors),
            fields_errors=errors
        ).complete()
