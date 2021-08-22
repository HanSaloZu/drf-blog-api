from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Ban


class BanSerializer(serializers.ModelSerializer):
    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=False,
        max_length=250,
        error_messages={
            "null": "Reason cannot be null",
            "invalid": "Invalid value for reason",
            "max_length": "Reason must be up to 250 characters long"
        }
    )

    class Meta:
        model = Ban
        fields = ["reason"]


class BannedUserSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    creator = UserSerializer()
    bannedAt = serializers.SerializerMethodField()

    def get_bannedAt(self, obj):
        return obj.banned_at

    class Meta:
        model = Ban
        fields = ["receiver", "reason", "bannedAt", "creator"]
