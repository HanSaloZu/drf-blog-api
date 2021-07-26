from django.core.files import File
from rest_framework.response import Response

from utils.exceptions import InvalidData400

from .services.images import update_image


class UpdateImageMixin:
    image_field = None

    def put(self, request):
        image = request.data.get(self.image_field)

        if isinstance(image, File):
            instance = self.get_object(request)
            link = update_image(instance, image)

            return Response({self.image_field: link})

        raise InvalidData400("File not provided",
                             {self.image_field: ["File not provided"]})
