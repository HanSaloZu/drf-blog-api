from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response


def custom_exception_handler(exc, context=None):
    if isinstance(exc, CustomAPIException):
        data = {
            "code": exc.code,
            "messages": exc.messages,
            "fieldsErrors": exc.fields_errors
        }

        return Response(data, status=exc.status_code,  content_type="application/json")

    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class CustomAPIException(Exception):
    code = "clientError"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, messages=[], fields_errors={}):
        if not hasattr(self, "messages"):
            if isinstance(messages, (list, tuple)):
                self.messages = messages
            else:
                self.messages = [messages]

        self.fields_errors = fields_errors

    def __str__(self):
        return f"API Exception: {self.status_code}:{self.code}"


class NotAuthenticated401(CustomAPIException):
    code = "notAuthenticated"
    status_code = status.HTTP_401_UNAUTHORIZED
    messages = ["You are not authenticated"]


class NotFound404(CustomAPIException):
    code = "notFound"
    status_code = status.HTTP_404_NOT_FOUND


class InvalidData400(CustomAPIException):
    code = "invalid"
    status_code = status.HTTP_400_BAD_REQUEST


class Forbidden403(CustomAPIException):
    code = "forbidden"
    status_code = status.HTTP_403_FORBIDDEN


class InactiveProfile403(CustomAPIException):
    code = "inactiveProfile"
    status_code = status.HTTP_403_FORBIDDEN
    messages = ["Your profile is not activated"]
