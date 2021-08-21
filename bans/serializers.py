from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Ban


class BannedUserSerializer(serializers.ModelSerializer):
    receiver = UserSerializer()
    creator = UserSerializer()
    bannedAt = serializers.SerializerMethodField()

    def get_bannedAt(self, obj):
        return obj.banned_at

    class Meta:
        model = Ban
        fields = ["receiver", "reason", "bannedAt", "creator"]
