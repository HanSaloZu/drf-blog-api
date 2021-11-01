from django.core.files import File
from rest_framework.response import Response

from utils.exceptions import BadRequest400

from .services.images import update_instance_image


class UpdateImageMixin:
    image_field = None

    def put(self, request):
        image = request.data.get(self.image_field)

        if isinstance(image, File):
            instance = self.get_object(request)
            link_to_image = update_instance_image(instance, image)

            return Response({self.image_field: link_to_image})

        raise BadRequest400("File not provided",
                            {self.image_field: ["File not provided"]})
