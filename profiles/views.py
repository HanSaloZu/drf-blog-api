from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.core.files import File

from utils.views import LoginRequiredAPIView
from utils.exceptions import InvalidData400
from utils.shortcuts import raise_400_based_on_serializer

from .services.photos import update_photo
from .serializers import (UpdateProfileSerializer, ProfileSerializer,
                          PreferencesSerializer, UpdatePasswordSerailizer)


class RetrieveUpdateProfileAPIView(LoginRequiredAPIView, APIView):
    """
    Retrieves and updates the authenticated user profile
    """

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

    def patch(self, request):
        instance = request.user.profile
        serializer = UpdateProfileSerializer(instance, data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(ProfileSerializer(instance).data)

        raise_400_based_on_serializer(serializer)


class UpdatePhotoAPIView(LoginRequiredAPIView, APIView):
    """
    Updates the photo of the authenticated user
    """

    def put(self, request):
        image = request.data.get("image")

        if isinstance(image, File):
            instance = request.user.profile.photo
            link = update_photo(instance, image)

            return Response({"photo": link})

        raise InvalidData400("File not provided",
                             {"image": "File not provided"})


class RetrieveUpdatePreferencesAPIView(LoginRequiredAPIView, APIView):
    """
    Retrieves and updates the authenticated user preferences
    """

    def get(self, request):
        serializer = PreferencesSerializer(request.user.profile.preferences)
        return Response(serializer.data)

    def put(self, request):
        instance = request.user.profile.preferences
        serializer = PreferencesSerializer(instance, data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            return Response(PreferencesSerializer(instance).data)

        raise_400_based_on_serializer(serializer)


class UpdatePasswordAPIView(LoginRequiredAPIView, APIView):
    """
    Updates the password of the authenticated user
    """

    def put(self, request):
        instance = request.user
        serializer = UpdatePasswordSerailizer(
            instance, data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)
