from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate, login, logout

from profiles.serializers import ProfileSerializer
from utils.exceptions import InvalidData400
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import LoginSerializer


class AuthenticationAPIView(APIView):
    def put(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(
                email=validated_data["email"],
                password=validated_data["password"]
            )

            if user:
                login(request, user)
                return Response(ProfileSerializer(user.profile).data)

            raise InvalidData400("Incorrect email or password")

        raise_400_based_on_serializer(serializer)

    def delete(self, request):
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)
