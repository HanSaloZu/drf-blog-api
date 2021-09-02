from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def get_error_messages_for_login_serializer(field_name):
    return {
        "required": f"Enter your {field_name}",
        "blank": f"Enter your {field_name}",
        "null": f"Enter your {field_name}",
        "invalid": f"Invalid {field_name}"
    }


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        allow_null=False,
        error_messages=get_error_messages_for_login_serializer("email")
    )

    password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages=get_error_messages_for_login_serializer("password")
    )

    class Meta:
        model = User
        fields = ["email", "password"]
