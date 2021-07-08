from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def get_error_messages(field_name):
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
        error_messages=get_error_messages("email")
    )

    password = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
        error_messages=get_error_messages("password")
    )

    class Meta:
        model = User
        fields = ["email", "password"]


def get_error_messages_for_registration_serializer(field_name, extend):
    capitalized_field_name = field_name.capitalize()
    error_messages = {
        "required": f"{capitalized_field_name} field is required",
        "blank": f"{capitalized_field_name} can't be empty",
        "null": f"{capitalized_field_name} is required",
    }
    error_messages.update(extend)

    return error_messages


class RegistrationSerializer(serializers.Serializer):
    login = serializers.SlugField(
        max_length=150,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages=get_error_messages_for_registration_serializer("login", {
            "max_length": "Login must be up to 150 characters long",
            "invalid": "Login can only contain letters, numbers, underscores and hyphens"
        })
    )

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        allow_null=False,
        required=True,
        error_messages=get_error_messages_for_registration_serializer("email", {
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
        error_messages=get_error_messages_for_registration_serializer("password", {
            "min_length": "Password must be at least 4 characters",
            "max_length": "Password must be up to 128 characters long"
        })
    )

    password2 = serializers.CharField(
        required=True,
        error_messages={
            "required": "You should repeat your password"
        })

    aboutMe = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        required=True,
        min_length=70,
        error_messages=get_error_messages_for_registration_serializer("about me", {
            "min_length": "About me must be at least 70 characters"
        })
    )

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
        instance.profile.about_me = validated_data["aboutMe"]
        instance.save()

        return instance
