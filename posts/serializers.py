from django.http import QueryDict
from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Like, Post
from .services import (create_post_attachment, delete_post_attachments,
                       get_post_attachments_list)


def generate_error_messages(field_name):
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
        return get_post_attachments_list(obj)

    class Meta:
        model = Post
        fields = ("id", "body", "likes", "createdAt",
                  "updatedAt", "isLiked", "attachments", "author")


class BaseCreateUpdatePostSerializer(serializers.Serializer):
    body = serializers.CharField(
        required=False,
        max_length=2000,
        allow_blank=True,
        allow_null=False,
        error_messages=generate_error_messages("body")
    )

    attachments = serializers.ListField(
        child=serializers.ImageField(
            error_messages={
                "invalid_image": "Invalid image in attached files"
            }
        ),
        required=False,
        allow_empty=True,
        max_length=5,
        error_messages=generate_error_messages("attachments") | {
            "invalid": "The submitted data was not a file"
        }
    )

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


class CreatePostSerializer(BaseCreateUpdatePostSerializer):
    class Meta:
        fields = ("body", "attachments")

    def validate(self, data):
        data["body"] = data.get("body", "")
        data["attachments"] = data.get("attachments", [])

        if len(data["body"]) == 0 and len(data["attachments"]) == 0:
            msg = "One of the two fields (body, attachments) cannot be empty"
            raise serializers.ValidationError({"body": msg})

        return data

    def create(self, validated_data):
        instance = Post.objects.create(
            author=self.context.get("request").user,
            body=validated_data.get("body", "")
        )

        for attachment in validated_data.get("attachments", []):
            create_post_attachment(instance, attachment)

        return instance


class UpdatePostSerializer(BaseCreateUpdatePostSerializer):
    class Meta:
        fields = ("body", "attachments")

    def validate(self, data):
        if not data:
            return data

        post_body = data.get("body", self.instance.body)
        post_attachments = data.get(
            "attachments", get_post_attachments_list(self.instance))

        if len(post_body) == 0 and len(post_attachments) == 0:
            msg = "One of the two fields (body, attachments) cannot be empty"
            raise serializers.ValidationError({"body": msg})

        return data

    def update(self, instance, validated_data):
        instance.body = validated_data.get("body", instance.body)

        if "attachments" in validated_data:
            delete_post_attachments(instance)

            for attachment in validated_data["attachments"]:
                create_post_attachment(instance, attachment)

        instance.save()
        return instance
