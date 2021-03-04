from rest_framework import serializers

from profiles.serializers import PhotosSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "login", "email"]


class LoginSerializer(serializers.Serializer):
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
    rememberMe = serializers.BooleanField(
        required=False,
        default=False,
        error_messages={
            "invalid": "Invalid value for rememberMe"
        })

    class Meta:
        model = User
        fields = ["email", "password", "rememberMe"]


class UsersListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.login

    def get_photos(self, obj):
        return PhotosSerializer(obj.profile.photos).data

    def get_status(self, obj):
        return obj.profile.status

    class Meta:
        model = User
        fields = ["name", "id", "photos", "status"]
