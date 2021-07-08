from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate, login, logout

from profiles.serializers import ProfileSerializer
from utils.exceptions import InvalidData400
from utils.shortcuts import raise_400_based_on_serializer

from .services.email import send_profile_activation_email
from .services.activation import get_user_by_uidb64_or_none
from .serializers import LoginSerializer, RegistrationSerializer
from .tokens import confirmation_token


class AuthenticationAPIView(APIView):
    def post(self, request):
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
                login(request, user)
                return Response(ProfileSerializer(user.profile).data)

            raise InvalidData400("Incorrect email or password")

        raise_400_based_on_serializer(serializer)

    def delete(self, request):
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)


class ProfileActivationAPIView(APIView):
    def post(self, request):
        user = get_user_by_uidb64_or_none(request.data.get("uidb64", ""))
        token = request.data.get("token", "")

        if user is not None and confirmation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return Response(status=HTTP_204_NO_CONTENT)

        raise InvalidData400("Invalid credentials")
