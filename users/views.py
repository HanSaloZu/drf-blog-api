from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from utils.views import LoginRequiredAPIView, ListAPIViewMixin
from utils.responses import NotFound404Response
from profiles.serializers import ProfileSerializer
from profiles.selectors import get_profile_by_user_login

from .serializers import UserSerializer


class UsersListAPIView(LoginRequiredAPIView, ListAPIViewMixin, APIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def filter_queryset(self, queryset, kwargs):
        return queryset.filter(login__contains=kwargs["q"])


class RetrieveUserProfileAPIView(LoginRequiredAPIView, RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = get_profile_by_user_login(kwargs["login"])

            serializer = ProfileSerializer(instance)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return NotFound404Response(messages=["Invalid login, user is not found"]).complete()
