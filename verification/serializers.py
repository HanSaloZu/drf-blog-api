from rest_framework import serializers

from .services.codes import (check_if_verification_code_exists,
                             remove_expired_codes)


class VerificationCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
        error_messages={
            "required": "Verification code field is required",
            "blank": "Verification code cannot be empty",
            "null": "Verification code cannot be null",
            "invalid": "Verification code is invalid or expired"
        }
    )

    def validate(self, data):
        remove_expired_codes()

        if not check_if_verification_code_exists(data["code"]):
            raise serializers.ValidationError(
                {"code": "Verification code is invalid or expired"})

        return data

    class Meta:
        fields = ("code",)
