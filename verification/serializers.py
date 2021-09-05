import datetime
from rest_framework import serializers

from .models import VerificationCode
from .services.codes import remove_expired_codes


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

        if not VerificationCode.objects.all().filter(
            code=data["code"]
        ).exists():
            raise serializers.ValidationError(
                {"code": "Verification code is invalid or expired"})

        return data

    class Meta:
        fields = ["code"]
