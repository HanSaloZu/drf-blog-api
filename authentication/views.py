from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError

from utils.exceptions import BadRequest400, NotAuthenticated401
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import (CustomTokenObtainPairSerializer,
                          CustomTokenRefreshSerializer)
from .services import (get_user_from_access_token_or_401,
                       raise_403_if_user_is_banned,
                       raise_403_if_user_is_inactive)


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
                raise_403_if_user_is_banned(user)
                raise_403_if_user_is_inactive(user)

                token = serializer.get_token(user)
                return Response({
                    "refresh": str(token),
                    "access": str(token.access_token)
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
                user = get_user_from_access_token_or_401(
                    serializer.validated_data["access"]
                )
                raise_403_if_user_is_inactive(user)
                raise_403_if_user_is_banned(user)

                return Response(serializer.validated_data)

            raise_400_based_on_serializer(serializer)
        except TokenError:
            raise NotAuthenticated401
