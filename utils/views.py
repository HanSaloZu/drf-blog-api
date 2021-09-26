from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from .exceptions import (Forbidden403, BadRequest400, NotAuthenticated401,
                         get_exception_json_response)


class LoginRequiredAPIView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return get_exception_json_response(NotAuthenticated401)

        return super().dispatch(request, *args, **kwargs)


class AdminRequiredAPIView(LoginRequiredAPIView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return get_exception_json_response(
                Forbidden403,
                ["You don't have permission to access this resource"]
            )

        return super().dispatch(request, *args, **kwargs)


class ListAPIViewMixin(APIView):
    serializer_class = None
    queryset = None

    def get_queryset(self):
        return self.queryset

    def get(self, request, *args, **kwargs):
        """
        Query parameters:

            q - search string
            limit - number of items per page
            page - page number
            ordering - list sorting
        """
        kwargs["q"] = request.query_params.get("q", "")
        kwargs["ordering"] = request.query_params.get("ordering", "")

        try:
            kwargs["limit"] = int(request.query_params.get("limit", 10))
        except ValueError:
            raise BadRequest400("Invalid limit value")

        if kwargs["limit"] > 100:
            raise BadRequest400("Maximum page size is 100 items")
        elif kwargs["limit"] < 1:
            raise BadRequest400("Minimum page size is 1 item")

        try:
            kwargs["page"] = int(request.query_params.get("page", 1))
        except ValueError:
            raise BadRequest400("Invalid page number value")

        queryset = self.filter_queryset(self.get_queryset(), kwargs)

        paginator = Paginator(queryset, kwargs["limit"])
        page = paginator.get_page(kwargs["page"])
        page_size = len(page.object_list)

        serializer = self.serializer_class(
            page, many=True, context={"request": request})

        return Response({
            "items": serializer.data,
            "totalItems": paginator.count,
            "totalPages": paginator.num_pages,
            "pageSize": page_size,
            "pageNumber": page.number
        })
