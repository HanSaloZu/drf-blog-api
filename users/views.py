from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer, LoginSerializer
from utils.response import APIResponse


@api_view(["GET"])
def user_detail(request, format=None):  # auth/me
    user = request.user
    response = APIResponse()

    if user.is_anonymous:
        response.result_code = 1
        response.messages.append("You are not authorized")
        return response.complete()

    response.data = UserSerializer(user).data
    return response.complete()


@api_view(["POST", "DELETE"])
def user_authentication(request):
    response = APIResponse()

    if request.method == "POST":  # login
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = authenticate(
                email=validated_data["email"], password=validated_data["password"])

            if user:
                login(request, user)

                if not validated_data["rememberMe"]:
                    request.session.set_expiry(0)

                response.data = {"userId": user.id}
                return response.complete()
            else:
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

    elif request.method == "DELETE":  # logout
        logout(request)
        return response.complete()
