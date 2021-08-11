from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Attachment, Post, Like


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    updatedAt = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    author = UserSerializer()

    def get_likes(self, obj):
        return Like.objects.all().filter(post=obj).count()

    def get_createdAt(self, obj):
        return obj.created_at

    def get_updatedAt(self, obj):
        return obj.updated_at

    def get_isLiked(self, obj):
        user = self.context.get("request").user
        return Like.objects.all().filter(post=obj, user=user).exists()

    def get_attachments(self, obj):
        return list(Attachment.objects.all().filter(
            post=obj
        ).values_list("link", flat=True))

    class Meta:
        model = Post
        fields = ["id", "title", "body", "likes", "createdAt",
                  "updatedAt", "isLiked", "attachments", "author"]
