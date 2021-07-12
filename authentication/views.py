from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate, login, logout

from profiles.serializers import ProfileSerializer
from utils.exceptions import InvalidData400, InactiveProfile403, Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .services.email import send_profile_activation_email
from .services.activation import activate_user_profile
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

            if user and user.is_active:
                login(request, user)
                return Response(ProfileSerializer(user.profile).data)
            elif user and not user.is_active:
                raise InactiveProfile403

            raise InvalidData400("Incorrect email or password")

        raise_400_based_on_serializer(serializer)

    def delete(self, request):
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)


class ProfileActivationAPIView(APIView):
    """
    Activates the user profile using the credentials sent by email after registration
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise Forbidden403("You are already authenticated")

        credentials = {
            "uidb64": request.data.get("uidb64", ""),
            "token": request.data.get("token", "")
        }
        user = activate_user_profile(credentials)
        if user is not None and user.is_active:
            return Response(status=HTTP_204_NO_CONTENT)

        raise InvalidData400("Invalid credentials")
