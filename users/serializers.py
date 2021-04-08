from rest_framework import serializers

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
    status = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.login

    def get_status(self, obj):
        return obj.profile.status

    def get_photo(self, obj):
        return obj.profile.photo.link

    class Meta:
        model = User
        fields = ["name", "id", "status", "photo"]
