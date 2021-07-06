from rest_framework import status


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
