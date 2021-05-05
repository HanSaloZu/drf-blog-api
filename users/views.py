from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.response import Response

from .selectors import get_all_users, get_users_by_term
from .serializers import UserSerializer, LoginSerializer, UsersListSerializer
from utils.response import APIResponse


class UserDetail(APIView):
    def get(self, request, format=None):
        user = request.user
        response = APIResponse()

        if user.is_anonymous:
            response.result_code = 1
            response.messages.append("You are not authorized")
            return response.complete()

        response.data = UserSerializer(user).data
        return response.complete()


class UserAuthentication(APIView):
    def post(self, request):
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


class UsersList(APIView):
    def get(self, request):
        count = int(request.GET.get("count", 10))
        page_number = int(request.GET.get("page", 1))
        term = request.GET.get("term", None)
        friend = {"true": True, "false": False}[  # the friend parameter can only be "true" or "false"
            request.GET.get("friend", "false")]

        response_data = {
            "items": [],
            "totalCount": 0,
            "error": ""
        }

        if count > 100:
            response_data["error"] = "Max page size is 100 items"
            return Response(response_data)

        if term:
            users_list = get_users_by_term(term)
        else:
            users_list = get_all_users()

        if friend:
            if not request.user.is_authenticated:
                return Response(response_data)

            followings = request.user.following.only("following_user")
            followings_ids = [i.following_user.id for i in list(followings)]
            users_list = users_list.filter(id__in=followings_ids)

        paginator = Paginator(users_list, count)
        page = paginator.get_page(page_number)

        for obj in page.object_list:
            user_data = UsersListSerializer(obj).data
            followed = False
            if request.user.is_authenticated:
                followed = obj.followers.all().filter(follower_user=request.user).exists()

            user_data.update({"followed": followed})
            response_data["items"].append(user_data)

        response_data["totalCount"] = users_list.count()
        return Response(response_data)
