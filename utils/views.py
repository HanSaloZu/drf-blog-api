from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status


class CustomLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = Response(
                {"message": "Authorization has been denied for this request."},
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json")
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}

            return response
        return super().dispatch(request, *args, **kwargs)
