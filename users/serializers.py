from rest_framework import serializers

from .models import User


class UsersListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    followed = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.login

    def get_status(self, obj):
        return obj.profile.status

    def get_photo(self, obj):
        return obj.profile.photo.link

    def get_followed(self, obj):
        user = self.context.get("request").user
        return obj.followers.all().filter(follower_user=user).exists()

    class Meta:
        model = User
        fields = ["name", "id", "status", "photo", "followed"]
