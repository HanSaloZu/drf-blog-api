from utils.views import ListAPIViewMixin, AdminRequiredAPIView

from .serializers import BannedUserSerializer
from .models import Ban


class ListBannedUsersAPIView(AdminRequiredAPIView, ListAPIViewMixin):
    serializer_class = BannedUserSerializer
    queryset = Ban.objects.all()

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(
            receiver__login__contains=kwargs["q"]
        ) | queryset.filter(
            creator__login__contains=kwargs["q"]
        ) | queryset.filter(
            reason__icontains=kwargs["q"]
        )
