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
