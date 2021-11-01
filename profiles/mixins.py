from django.core.files import File
from rest_framework.response import Response

from utils.exceptions import BadRequest400

from .services.images import update_instance_image


class UpdateImageMixin:
    image_field = None

    def put(self, request):
        image = request.data.get(self.image_field)

        if image.content_type.split("/")[0] == "image":
            instance = self.get_object(request)
            link_to_image = update_instance_image(instance, image)

            return Response({self.image_field: link_to_image})

        raise BadRequest400("Image not provided",
                            {self.image_field: ["Image not provided"]})
