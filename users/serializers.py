from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Please enter your Email",
            "null": "Please enter your Email",
            "invalid": "Enter valid Email"
        })
    password = serializers.CharField(
        required=True,
        error_messages={
            "required": "Enter your password",
            "null": "Enter your password"
        })

    class Meta:
        model = User
        fields = ["email", "password"]


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
