from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions import NotFound404

from .models import Post


def get_post_by_id_or_404(id):
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        raise NotFound404("Invalid id, post is not found")
