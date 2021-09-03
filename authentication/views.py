from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from bans.services import is_banned
from utils.exceptions import BadRequest400, Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import CustomTokenObtainPairSerializer


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
