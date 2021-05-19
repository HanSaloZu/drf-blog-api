from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .serializers import UserSerializer, LoginSerializer, UsersListSerializer
from utils.response import APIResponse
from utils.views import CustomLoginRequiredMixin

User = get_user_model()


class UserAuthentication(APIView):
    def get(self, request):
        user = request.user
        response = APIResponse()

        if user.is_anonymous:
            response.result_code = 1
            response.messages.append("You are not authorized")
            return response.complete()

        response.data = UserSerializer(user).data
        return response.complete()

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


class UsersList(CustomLoginRequiredMixin, generics.ListAPIView):
    serializer_class = UsersListSerializer

    def validate_parameters(self):
        term = self.request.GET.get("term", "")
        friend = self.request.GET.get("friend", "false")
        # the friend parameter can only be "true" or "false"

        if friend != "false" and friend != "true":
            raise ValidationError(detail="Invalid friend flag value")
        friend = {"true": True, "false": False}[friend]

        try:
            count = int(self.request.GET.get("count", 10))
        except ValueError:
            raise ValidationError(detail="Invalid count value")

        try:
            page_number = int(self.request.GET.get("page", 1))
        except ValueError:
            raise ValidationError(detail="Invalid page number value")

        if count > 100:
            raise ValidationError(detail="Maximum page size is 100 items")
        elif count < 0:
            raise ValidationError(detail="Minimum page size is 0 items")

        self.get_parameters = {"term": term, "friend": friend,
                               "count": count, "page_number": page_number}

    def get_queryset(self):
        self.validate_parameters()
        return User.objects.all()

    def filter_queryset(self, queryset):
        filtered_queryset = queryset.filter(
            login__contains=self.get_parameters["term"])
        if self.get_parameters["friend"]:
            followings = self.request.user.following.only("following_user")
            followings_ids = [i.following_user.id for i in list(followings)]
            filtered_queryset = filtered_queryset.filter(id__in=followings_ids)

        self.total_count = filtered_queryset.count()
        return filtered_queryset

    def paginate_queryset(self, queryset):
        paginator = Paginator(queryset, self.get_parameters["count"])
        return paginator.get_page(self.get_parameters["page_number"])

    def get_paginated_response(self, serialized_data):
        return Response({"items": serialized_data, "totalCount": self.total_count})
