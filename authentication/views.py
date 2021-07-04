from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from django.contrib.auth import authenticate, login, logout

from profiles.serializers import ProfileSerializer
from utils.responses import InvalidData400Response
from utils.shortcuts import generate_messages_list_by_serializer_errors

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

            return InvalidData400Response(messages=["Incorrect email or password"]).complete()

        errors = serializer.errors
        return InvalidData400Response(
            messages=generate_messages_list_by_serializer_errors(errors),
            fields_errors=errors
        ).complete()

    def delete(self, request):
        logout(request)
        return Response(status=HTTP_204_NO_CONTENT)
