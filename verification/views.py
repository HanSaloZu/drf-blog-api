from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from utils.exceptions import Forbidden403
from utils.shortcuts import raise_400_based_on_serializer

from .serializers import VerificationCodeSerializer
from .services.codes import remove_expired_codes, verify_email_by_code


class EmailVerificationAPIView(APIView):
    """
    Activates the user by the code sent by email after registration
    """

    def post(self, request):
        if request.user.is_authenticated:
            raise Forbidden403("You are already authenticated")

        remove_expired_codes()
        serializer = VerificationCodeSerializer(data=request.data)

        if serializer.is_valid():
            verify_email_by_code(serializer.validated_data["code"])
            return Response(status=HTTP_204_NO_CONTENT)

        raise_400_based_on_serializer(serializer)
