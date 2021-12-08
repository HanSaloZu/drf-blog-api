from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from profiles.selectors import get_profile_by_user_login_or_404
from utils.exceptions import Forbidden403
from utils.shortcuts import raise_400_based_on_serializer
from utils.views import AdminRequiredAPIView, ListAPIViewMixin

from .models import Ban
from .selectors import get_ban_object_by_login_or_404
from .serializers import BannedUserSerializer, BanSerializer
from .services import ban_user, check_if_user_is_banned, unban_user


class ListBannedUsersAPIView(AdminRequiredAPIView, ListAPIViewMixin):
    """
    Lists all banned users
    """

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


class BanAPIView(AdminRequiredAPIView, APIView):
    """
    Creates, retrieves, updates, or deletes the specified ban
    """

    def get(self, request, login):
        instance = get_ban_object_by_login_or_404(login)
        return Response(BannedUserSerializer(instance).data)

    def put(self, request, login):
        receiver = get_profile_by_user_login_or_404(login).user

        if check_if_user_is_banned(receiver):
            instance = get_ban_object_by_login_or_404(login)
            serializer = BanSerializer(instance, request.data)

            if serializer.is_valid():
                instance = serializer.save()
                return Response(BannedUserSerializer(instance).data)

            raise_400_based_on_serializer(serializer)

        if receiver.is_staff:
            raise Forbidden403("Admins cannot be banned")

        serializer = BanSerializer(data=request.data)
        if serializer.is_valid():
            ban_object = ban_user(receiver=receiver, creator=self.request.user,
                                  reason=serializer.validated_data["reason"])
            return Response(BannedUserSerializer(ban_object).data,
                            status=HTTP_201_CREATED)

        raise_400_based_on_serializer(serializer)

    def delete(self, request, login):
        instance = get_ban_object_by_login_or_404(login)
        unban_user(instance.receiver)

        return Response(status=HTTP_204_NO_CONTENT)
