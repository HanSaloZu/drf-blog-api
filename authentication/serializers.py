from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

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
