from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout

from .serializers import LoginSerializer
from utils.response import APIResponse


class UserAuthentication(APIView):
    def put(self, request):
        response = APIResponse()
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(
                email=validated_data["email"], password=validated_data["password"])
            if user:
                login(request, user)

                response.data = {"userId": user.id}
                return response.complete()

            response.result_code = 1
            response.messages.append("Incorrect Email or Password")
            return response.complete()

        fields_errors = serializer.errors
        for field in fields_errors:
            message = fields_errors[field][0]
            response.messages.append(message)
            response.fields_errors.append({
                "field": field,
                "error": message
            })

        response.result_code = 1
        return response.complete()

    def delete(self, request):
        response = APIResponse()
        logout(request)
        return response.complete()
