from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED

from utils.views import ListAPIViewMixin, AdminRequiredAPIView
from utils.shortcuts import raise_400_based_on_serializer
from utils.exceptions import Forbidden403, BadRequest400
from profiles.selectors import get_profile_by_user_login_or_404

from .serializers import BanSerializer, BannedUserSerializer
from .models import Ban
from .services import unban, is_banned, ban
from .selectors import get_ban_object_by_login_or_404


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

        if is_banned(receiver):
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
            ban_object = ban(receiver=receiver, creator=self.request.user,
                             reason=serializer.validated_data["reason"])
            return Response(BannedUserSerializer(ban_object).data,
                            status=HTTP_201_CREATED)

        raise_400_based_on_serializer(serializer)

    def delete(self, request, login):
        instance = get_ban_object_by_login_or_404(login)
        unban(instance.receiver)

        return Response(status=HTTP_204_NO_CONTENT)
