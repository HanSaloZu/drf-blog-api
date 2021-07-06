from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.core.paginator import Paginator

from .exceptions import NotAuthenticated401, InvalidData400, custom_exception_handler


class LoginRequiredAPIView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = custom_exception_handler(NotAuthenticated401())
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}

            return response

        return super().dispatch(request, *args, **kwargs)


class ListAPIViewMixin:
    serializer_class = None
    queryset = None

    def get(self, request):
        """
        Query parameters:

            q - search string
            limit - number of items per page
            page - page number
        """
        kwargs = {"q": request.GET.get("q", "")}

        try:
            kwargs["limit"] = int(request.GET.get("limit", 10))
        except ValueError:
            return InvalidData400Response(messages=["Invalid limit value"]).complete()

        if kwargs["limit"] > 100:
            return InvalidData400Response(messages=["Maximum page size is 100 items"]).complete()
        elif kwargs["limit"] < 0:
            return InvalidData400Response(messages=["Minimum page size is 0 items"]).complete()

        try:
            kwargs["page"] = int(request.GET.get("page", 1))
        except ValueError:
            return InvalidData400Response(messages=["Invalid page number value"]).complete()

        queryset = self.filter_queryset(self.queryset, kwargs)

        paginator = Paginator(queryset, kwargs["limit"])
        page = paginator.get_page(kwargs["page"])

        serializer = self.serializer_class(
            page, many=True, context={"request": request})

        return Response({
            "items": serializer.data,
            "page": {
                "totalItems": paginator.count,  # total number of items, across all pages
                "totalPages": paginator.num_pages,

                # pageSize - number of items on the current page
                "pageSize": len(page.object_list),

                "pageNumber": page.number
            }
        })
