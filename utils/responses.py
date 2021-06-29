from rest_framework.response import Response


class ClientErrorResponse:
    def __init__(self):
        self.detail = ""
        self.messages = []
        self.fields_errors = {}
        self.status_code = 400

    def complete(self):
        return Response({
            "detail": self.detail,
            "messages": self.messages,
            "fieldsErrors": self.fields_errors,
        }, status=self.status_code, content_type="application/json")
