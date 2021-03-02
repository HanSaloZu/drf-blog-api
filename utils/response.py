from rest_framework.response import Response


class APIResponse:
    def __init__(self):
        self.data = {}
        self.messages = []
        self.fields_errors = []
        self.result_code = 0

    def complete(self):
        return Response({
            "data": self.data,
            "messages": self.messages,
            "fieldsErrors": self.fields_errors,
            "resultCode": self.result_code
        })
