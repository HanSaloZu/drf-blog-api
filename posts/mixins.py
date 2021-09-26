from django.db.models import Count

from utils.views import ListAPIViewMixin

from .serializers import PostSerializer
from .models import Post


class ListPostsAPIViewMixin(ListAPIViewMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(body__icontains=kwargs["q"])


class ListPostsWithOrderingAPIViewMixin(ListPostsAPIViewMixin):
    """
    This mixin allows order by list of posts by
    likes or creation date(created_at)
    """

    def filter_queryset(self, queryset, kwargs):
        allowed_ordering_fields = ["likes", "createdAt"]
        ordering_field = kwargs.get("ordering", None)

        if ordering_field:
            sign = ""
            if ordering_field.startswith("-"):
                sign = "-"
                ordering_field = ordering_field[1:]

            if ordering_field in allowed_ordering_fields:

                if ordering_field == "likes":
                    queryset = queryset.annotate(likes=Count("like"))
                    ordering_field = sign + ordering_field

                elif ordering_field == "createdAt":
                    ordering_field = sign + "created_at"

                queryset = queryset.order_by(ordering_field)

        return super().filter_queryset(queryset, kwargs)
