from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer


def get_exception_json_response(exception, messages=[]):
    response = custom_exception_handler(exception(messages))
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}

    return response


def custom_exception_handler(exc, context=None):
    default_response_data = {
        "code": "unhandledError",
        "messages": "Something went wrong",
        "fieldsErrors": {}
    }

    if isinstance(exc, CustomAPIException):
        return Response(
            data={
                "code": exc.code,
                "messages": exc.messages,
                "fieldsErrors": exc.fields_errors
            },
            status=exc.status_code,
            content_type="application/json"
        )

    response = exception_handler(exc, context)
    if response is not None:
        response.data = default_response_data | {
            "code": get_exception_code(exc),
            "messages": normalize_exception_detail(response.data["detail"])
        }

    return response


def get_exception_code(exc):
    if not hasattr(exc, "default_code"):
        return "error"

    return normalize_default_exception_code(exc.default_code)


def normalize_default_exception_code(default_code):
    normalized_code = ''.join(
        word.title() for word in default_code.split('_')
    )

    normalized_code = normalized_code[0].lower() + normalized_code[1::]
    return normalized_code


def normalize_exception_detail(exc_detail):
    if exc_detail.endswith("."):
        return exc_detail[0:-1:]
    return exc_detail


class CustomAPIException(Exception):
    code = "clientError"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, messages=[], fields_errors={}, code=""):
        if not hasattr(self, "messages"):
            if isinstance(messages, (list, tuple)):
                self.messages = messages
            else:
                self.messages = [messages]

        if code:
            self.code = code

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


class BadRequest400(CustomAPIException):
    code = "invalid"
    status_code = status.HTTP_400_BAD_REQUEST


class Forbidden403(CustomAPIException):
    code = "forbidden"
    status_code = status.HTTP_403_FORBIDDEN
