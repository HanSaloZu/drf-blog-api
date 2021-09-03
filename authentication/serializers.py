from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


def get_error_messages(field_name):
    return {
        "required": f"Enter your {field_name}",
        "blank": f"Enter your {field_name}",
        "null": f"Enter your {field_name}",
        "invalid": f"Invalid {field_name}"
    }


class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        allow_null=False,
        error_messages=get_error_messages("email")
    )

    password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages=get_error_messages("password")
    )

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    class Meta:
        fields = ["email", "password"]
