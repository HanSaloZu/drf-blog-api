from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import LoginSerializer, UsersListSerializer

User = get_user_model()


class UsersList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersListSerializer

    def validate_parameters(self):
        term = self.request.GET.get("term", "")

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

        self.get_parameters = {"term": term,
                               "count": count, "page_number": page_number}

    def get_queryset(self):
        self.validate_parameters()
        return User.objects.all()

    def filter_queryset(self, queryset):
        filtered_queryset = queryset.filter(
            login__contains=self.get_parameters["term"])
        self.total_count = filtered_queryset.count()

        return filtered_queryset

    def paginate_queryset(self, queryset):
        paginator = Paginator(queryset, self.get_parameters["count"])
        return paginator.get_page(self.get_parameters["page_number"])

    def get_paginated_response(self, serialized_data):
        return Response({"items": serialized_data, "totalCount": self.total_count})
