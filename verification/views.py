from rest_framework.response import Response
from rest_framework import status, views

from utils import exceptions as custom_exceptions
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import VerificationCodeSerializer
from .services.codes import verify_email_by_code


class EmailVerificationAPIView(views.APIView):
    """
    Activates the user by the code sent by email after registration
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise custom_exceptions.Forbidden403(
                "You are already authenticated"
            )

        serializer = VerificationCodeSerializer(data=request.data)

        if serializer.is_valid():
            verify_email_by_code(serializer.validated_data["code"])
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)
