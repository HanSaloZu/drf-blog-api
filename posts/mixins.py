from utils.views import ListAPIViewMixin

from .serializers import PostSerializer
from .models import Post


class ListPostsAPIViewMixin(ListAPIViewMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(
            title__icontains=kwargs["q"]
        ) | queryset.filter(
            body__icontains=kwargs["q"]
        )
