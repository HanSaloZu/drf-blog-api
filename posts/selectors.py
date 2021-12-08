from django.core.exceptions import ObjectDoesNotExist

from utils.exceptions import NotFound404

from .models import Like, Post


def get_post_by_id_or_404(id):
    try:
        return Post.objects.get(id=id)
    except ObjectDoesNotExist:
        raise NotFound404("Invalid id, post is not found")


def get_liked_posts(user):
    liked_posts_ids = Like.objects.all().filter(user=user).values_list("post")
    return Post.objects.all().filter(id__in=liked_posts_ids)
