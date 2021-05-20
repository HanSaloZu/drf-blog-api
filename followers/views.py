from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT

from .models import FollowersModel

User = get_user_model()


class FollowAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    model = FollowersModel

    def get(self, request, user_id):
        subject = get_object_or_404(User, id=user_id)
        return Response({"following": self.model.is_following(request.user, subject)})

    def post(self, request, user_id):
        subject = get_object_or_404(User, id=user_id)

        if user_id == request.user.id:
            raise ValidationError({"message": "You can't follow yourself"})
        elif self.model.is_following(request.user, subject):
            raise ValidationError(
                {"message": "You are already following this user"})

        self.model.follow(request.user, subject)
        return Response(status=HTTP_204_NO_CONTENT)

    def get_object(self):
        subject = get_object_or_404(User, id=self.kwargs["user_id"])

        if self.model.is_following(self.request.user, subject):
            return self.model.objects.filter(
                follower_user=self.request.user, following_user=subject)
        else:
            raise ValidationError(
                {"message": "You should first follow the user, then you can unfollow"})
