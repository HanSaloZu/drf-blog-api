from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


class ClientErrorResponse:
    def __init__(self, detail="", messages=[], fields_errors={}, status_code=HTTP_400_BAD_REQUEST,
                 content_type="application/json"):
        self.detail = detail
        self.messages = messages
        self.fields_errors = fields_errors
        self.status_code = status_code

    def complete(self):
        return Response({
            "detail": self.detail,
            "messages": self.messages,
            "fieldsErrors": self.fields_errors,
        }, status=self.status_code, content_type="application/json")
