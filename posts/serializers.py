from rest_framework import serializers
from django.http import QueryDict

from users.serializers import UserSerializer

from .models import Attachment, Post, Like
from .services import create_post_attachment, delete_post_attachments


def get_error_messages(field_name):
    capitalized_field_name = field_name.capitalize()

    return {
        "required": f"{capitalized_field_name} field is required",
        "null": f"{capitalized_field_name} field cannot be null",
        "blank": f"{capitalized_field_name} field cannot be empty",
        "invalid": f"Invalid value for {field_name} field",
        "max_length": f"{capitalized_field_name} field value is too long",
        "not_a_list": f"{capitalized_field_name} should be a list of items"
    }


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


class CreateUpdatePostSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        max_length=70,
        allow_blank=False,
        allow_null=False,
        error_messages=get_error_messages("title")
    )

    body = serializers.CharField(
        required=True,
        max_length=2000,
        allow_blank=True,
        allow_null=False,
        error_messages=get_error_messages("body")
    )

    attachments = serializers.ListField(
        required=False,
        child=serializers.ImageField(
            error_messages={
                "invalid_image": "Invalid image in attached files"
            }
        ),
        allow_empty=True,
        max_length=5,
        error_messages=get_error_messages("attachments")
    )

    class Meta:
        model = Post
        fields = ["title", "body", "attachments"]

    def to_internal_value(self, data):
        # Handling the case when {attachments: ['']} or {attachments: ''}

        if "attachments" in data:
            if isinstance(data, QueryDict):
                # get a dict representation of QueryDict
                data_dict = data.dict()
            else:
                data_dict = data.copy()

            if data_dict["attachments"] == "":
                data_dict["attachments"] = []
                return super().to_internal_value(data_dict)

        return super().to_internal_value(data)

    def create(self, validated_data):
        instance = Post.objects.create(
            author=self.context.get("request").user,
            title=validated_data["title"],
            body=validated_data.get("body", "")
        )

        for attachment in validated_data.get("attachments", []):
            create_post_attachment(instance, attachment)

        return instance

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)

        if "attachments" in validated_data:
            delete_post_attachments(instance)

            for attachment in validated_data["attachments"]:
                create_post_attachment(instance, attachment)

        instance.save()
        return instance
