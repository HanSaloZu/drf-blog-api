from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.paginator import Paginator

from .exceptions import (NotAuthenticated401, BadRequest400,
                         custom_exception_handler)


class LoginRequiredAPIView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = custom_exception_handler(NotAuthenticated401())
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}

            return response

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
        """
        kwargs["q"] = request.query_params.get("q", "")

        try:
            kwargs["limit"] = int(request.query_params.get("limit", 10))
        except ValueError:
            raise BadRequest400("Invalid limit value")

        if kwargs["limit"] > 100:
            raise BadRequest400("Maximum page size is 100 items")
        elif kwargs["limit"] < 0:
            raise BadRequest400("Minimum page size is 0 items")

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
            "totalItems": paginator.count,  # total number of items, across all pages
            "totalPages": paginator.num_pages,  # total number of pages
            "pageSize": page_size,  # number of items on the current page
            "pageNumber": page.number  # current page number
        })
