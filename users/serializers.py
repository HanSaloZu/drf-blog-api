from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    isAdmin = serializers.SerializerMethodField()

    def get_userId(self, obj):
        return obj.id

    def get_avatar(self, obj):
        return obj.profile.avatar.link

    def get_isAdmin(self, obj):
        return obj.is_staff

    class Meta:
        model = User
        fields = ("id", "login", "avatar", "isAdmin")


class ExtendedUserSerializer(UserSerializer):
    status = serializers.SerializerMethodField()
    isFollowed = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.profile.status

    def get_isFollowed(self, obj):
        user = self.context.get("request").user
        return obj.followers.all().filter(follower_user=user).exists()

    class Meta:
        model = User
        fields = ("id", "login", "status",
                  "avatar", "isAdmin", "isFollowed")


def generate_error_messages(field_name, extend):
    capitalized_field_name = field_name.capitalize()
    error_messages = {
        "required": f"{capitalized_field_name} field is required",
        "blank": f"{capitalized_field_name} can't be empty",
        "null": f"{capitalized_field_name} is required",
    }

    return error_messages | extend


class CreateUserSerializer(serializers.Serializer):
    login = serializers.SlugField(
        max_length=50,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages=generate_error_messages(
            "login", {
                "max_length": "Login must be up to 150 characters long",
                "invalid": ("Login can only contain English letters, " +
                            "numbers, underscores and hyphens")
            })
    )

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages=generate_error_messages(
            "email", {
                "invalid": "Enter a valid email",
                "max_length": "Email must be up to 254 characters long",
            })
    )

    password1 = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        min_length=4,
        max_length=128,
        error_messages=generate_error_messages(
            "password", {
                "min_length": "Password must be at least 4 characters",
                "max_length": "Password must be up to 128 characters long"
            })
    )

    password2 = serializers.CharField(
        required=True,
        error_messages={
            "required": "You should repeat your password"
        })

    def validate(self, data):
        if User.objects.all().filter(login=data["login"]).exists():
            raise serializers.ValidationError(
                {"login": "This login is already in use"})

        if User.objects.all().filter(email=data["email"]).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use"})

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                {"password2": "Passwords do not match"})

        return data

    def create(self, validated_data):
        instance = User.objects.create_user(
            login=validated_data["login"],
            email=validated_data["email"],
            password=validated_data["password1"],
            is_active=False
        )

        return instance
