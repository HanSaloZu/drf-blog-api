from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model

from utils.views import LoginRequiredAPIView, ListAPIViewMixin
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login_or_404

from .serializers import UserSerializer


class UsersListAPIView(LoginRequiredAPIView, ListAPIViewMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(login__contains=kwargs["q"])


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        instance = get_profile_by_user_login_or_404(kwargs["login"])
        serializer = ProfileSerializer(instance)

        return Response(serializer.data)
