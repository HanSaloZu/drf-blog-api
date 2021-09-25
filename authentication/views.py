from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError

from bans.services import is_banned
from utils.exceptions import BadRequest400, Forbidden403, NotAuthenticated401
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import (CustomTokenObtainPairSerializer,
                          CustomTokenRefreshSerializer)


class CustomObtainTokenPairAPIView(APIView):
    """
    Takes user credentials and returns an access and refresh
    JSON web token pair
    """

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(**validated_data)

            if user:
                if is_banned(user):
                    raise Forbidden403("You are banned")
                if not user.is_active:
                    raise Forbidden403("Your profile is not activated",
                                       code="inactiveProfile")

                refresh = serializer.get_token(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })

            raise BadRequest400("Incorrect email or password")

        raise_400_based_on_serializer(serializer)


class CustomTokenRefreshAPIView(APIView):
    """
    Takes a refresh JSON web token and returns an access JSON web token
    """

    def post(self, request):
        serializer = CustomTokenRefreshSerializer(data=request.data)

        try:
            if serializer.is_valid():
                return Response(serializer.validated_data)

            raise_400_based_on_serializer(serializer)
        except TokenError:
            raise NotAuthenticated401(code="invalidToken")
