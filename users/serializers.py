from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    isAdmin = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()

    def get_userId(self, obj):
        return obj.id

    def get_status(self, obj):
        return obj.profile.status

    def get_photo(self, obj):
        return obj.profile.photo.link

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isFollowed(self, obj):
        user = self.context.get("request").user
        return obj.followers.all().filter(follower_user=user).exists()

    class Meta:
        model = User
        fields = ["userId", "login", "status",
                  "photo", "isAdmin", "isFollowed"]
