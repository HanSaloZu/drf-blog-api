from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    isAdmin = serializers.SerializerMethodField()

    def get_userId(self, obj):
        return obj.id

    def get_avatar(self, obj):
        return obj.profile.avatar.link

    def get_isAdmin(self, obj):
        return obj.is_staff

    class Meta:
        model = User
        fields = ["id", "login", "avatar", "isAdmin"]


class ExtendedUserSerializer(UserSerializer):
    status = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.profile.status

    def get_isFollowed(self, obj):
        user = self.context.get("request").user
        return obj.followers.all().filter(follower_user=user).exists()

    class Meta:
        model = User
        fields = ["id", "login", "status",
                  "avatar", "isAdmin", "isFollowed"]
