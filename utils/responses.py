from rest_framework.response import Response
from rest_framework import status


class ClientErrorResponse:
    code = "clientError"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, messages=[], fields_errors={}):
        if not hasattr(self, "messages"):
            self.messages = messages
        self.fields_errors = fields_errors

    def __str__(self):
        return f"{self.code}"

    def complete(self):
        return Response({
            "code": self.code,
            "messages": self.messages,
            "fieldsErrors": self.fields_errors,
        }, status=self.status_code, content_type="application/json")


class NotAuthenticated401Response(ClientErrorResponse):
    code = "notAuthenticated"
    status_code = status.HTTP_401_UNAUTHORIZED
    messages = ["You are not authenticated"]


class NotFound404Response(ClientErrorResponse):
    code = "notFound"
    status_code = status.HTTP_404_NOT_FOUND


class InvalidData400Response(ClientErrorResponse):
    code = "invalid"
    status_code = status.HTTP_400_BAD_REQUEST
