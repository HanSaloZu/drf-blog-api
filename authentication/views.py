from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate, login, logout

from bans.services import is_banned
from profiles.serializers import AuthenticatedUserProfileSerializer
from utils.exceptions import BadRequest400, Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .services.email import send_profile_activation_email
from .serializers import LoginSerializer, RegistrationSerializer


class AuthenticationAPIView(APIView):
    """
    Basic authentication functionality

    Registration(POST)
    Login(PUT)
    Logout(DELETE)
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise Forbidden403("You are already authenticated")

        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_profile_activation_email(user)

            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)

    def put(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(
                email=validated_data["email"],
                password=validated_data["password"]
            )

            if user:
                if is_banned(user):
                    raise Forbidden403("You are banned")
                if not user.is_active:
                    raise Forbidden403("Your profile is not activated",
                                       code="inactiveProfile")

                login(request, user)
                return Response(
                    AuthenticatedUserProfileSerializer(user.profile).data
                )

            raise BadRequest400("Incorrect email or password")

        raise_400_based_on_serializer(serializer)

    def delete(self, request):
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)
