from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.response import Response

from .selectors import get_all_users, get_users_by_term
from .serializers import UserSerializer, LoginSerializer, UsersListSerializer
from utils.response import APIResponse
from following.selectors import get_all_user_followings
from following.service import is_following


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
        if request.data:
            serializer = LoginSerializer(data=request.data)
        else:
            serializer = LoginSerializer(data=request.query_params)

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


@api_view(["GET"])
def users_list(request):
    count = request.GET.get("count", 10)
    page_number = request.GET.get("page", 1)
    term = request.GET.get("term", None)
    friend = request.GET.get("friend", None)

    response_data = {
        "items": [],
        "totalCount": 0,
        "error": ""
    }

    if int(count) > 100:
        response_data["error"] = "Max page size is 100 items"
        return Response(response_data)

    if term:
        users_list = get_users_by_term(term)
    else:
        users_list = get_all_users()

    if friend:
        if not request.user.is_authenticated:
            return Response(response_data)

        followings = get_all_user_followings(request.user)
        followings_ids = [i.following_user.id for i in list(followings)]
        users_list = users_list.filter(id__in=followings_ids)

    total_count = users_list.count()
    paginator = Paginator(users_list, count)
    page = paginator.get_page(page_number)

    for obj in page.object_list:
        user_data = UsersListSerializer(obj).data
        followed = False
        if request.user.is_authenticated:
            followed = is_following(request.user, user_data["id"])

        user_data.update({"followed": followed})
        user_photos = user_data["photos"]
        if user_photos["small"] and user_photos["large"]:
            user_photos["small"] = request.scheme + "://" + \
                request.get_host() + user_photos["small"]
            user_photos["large"] = request.scheme + "://" + \
                request.get_host() + user_photos["large"]

        response_data["items"].append(user_data)

    response_data["totalCount"] = total_count
    return Response(response_data)
