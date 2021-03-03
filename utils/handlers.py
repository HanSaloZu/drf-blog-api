from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response = Response({"message": "An error has occurred."},
                            status=status_code)

    return response
