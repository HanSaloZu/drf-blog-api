from django.contrib.auth import get_user_model

from utils.views import ListAPIViewMixin

from .serializers import ExtendedUserSerializer

User = get_user_model()


class ListUsersAPIViewMixin(ListAPIViewMixin):
    queryset = User.objects.all()
    serializer_class = ExtendedUserSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(login__contains=kwargs["q"])
