from rest_framework.renderers import JSONRenderer

from .responses import NotAuthenticated401Response


class LoginRequiredAPIView:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            response = NotAuthenticated401Response().complete()
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}

            return response

        return super().dispatch(request, *args, **kwargs)
