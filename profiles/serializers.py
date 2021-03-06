from rest_framework import serializers

from bans.services import check_if_user_is_banned

from .models import Contacts, Profile


def generate_error_messages(field_name):
    capitalized_field_name = field_name.capitalize()

    return {
        "required": f"{capitalized_field_name} field is required",
        "null": f"{capitalized_field_name} field cannot be null",
        "blank": f"{capitalized_field_name} field cannot be empty",
        "invalid": f"Invalid value for {field_name} field",
        "max_length": f"{capitalized_field_name} field value is too long",
        "min_length": f"{capitalized_field_name} field value is too short",
    }


class ContactsSerializer(serializers.ModelSerializer):
    mainLink = serializers.SerializerMethodField()

    def get_mainLink(self, obj):
        return obj.main_link

    class Meta:
        model = Contacts
        fields = ("github", "vk", "facebook",
                  "instagram", "twitter", "website", "youtube", "mainLink")


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    login = serializers.SerializerMethodField()
    isLookingForAJob = serializers.SerializerMethodField()
    professionalSkills = serializers.SerializerMethodField()
    isAdmin = serializers.SerializerMethodField()
    isBanned = serializers.SerializerMethodField()
    aboutMe = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    contacts = ContactsSerializer()

    def get_id(self, obj):
        return obj.user.id

    def get_login(self, obj):
        return obj.user.login

    def get_isLookingForAJob(self, obj):
        return obj.is_looking_for_a_job

    def get_professionalSkills(self, obj):
        return obj.professional_skills

    def get_isAdmin(self, obj):
        return obj.user.is_staff

    def get_isBanned(self, obj):
        return check_if_user_is_banned(obj.user)

    def get_aboutMe(self, obj):
        return obj.about_me

    def get_avatar(self, obj):
        return obj.avatar.link

    def get_banner(self, obj):
        return obj.banner.link

    class Meta:
        model = Profile
        fields = ("id", "isLookingForAJob", "professionalSkills", "isAdmin",
                  "fullname", "login", "status", "location", "birthday",
                  "isBanned", "aboutMe", "avatar", "banner", "contacts")


class AuthenticatedUserProfileSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = ("id", "isLookingForAJob", "professionalSkills", "isAdmin",
                  "fullname", "login", "status", "location", "birthday",
                  "aboutMe", "theme", "avatar", "banner", "contacts")


class UpdateContactsSerializer(serializers.Serializer):
    github, vk, facebook, instagram, twitter, website, youtube, mainLink = [
        serializers.URLField(
            max_length=200,
            required=False,
            allow_blank=True,
            error_messages=generate_error_messages(field)) for field in [
            "github",
            "vk",
            "facebook",
            "instagram",
            "twitter",
            "website",
            "youtube",
            "mainLink"
        ]
    ]


class UpdateProfileSerializer(serializers.Serializer):
    isLookingForAJob = serializers.BooleanField(
        required=False,
        allow_null=False,
        error_messages=generate_error_messages("is looking for a job")
    )

    professionalSkills = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=350,
        allow_null=False,
        error_messages=generate_error_messages("professional skills")
    )

    fullname = serializers.CharField(
        required=False,
        max_length=150,
        allow_blank=False,
        allow_null=False,
        error_messages=generate_error_messages("fullname")
    )

    status = serializers.CharField(
        required=False,
        max_length=70,
        allow_null=False,
        allow_blank=True,
        error_messages=generate_error_messages("status")
    )

    aboutMe = serializers.CharField(
        required=False,
        max_length=800,
        allow_blank=True,
        allow_null=False,
        error_messages=generate_error_messages("about me")
    )

    birthday = serializers.DateField(
        format="YYYY-MM-DD",
        allow_null=True,
        required=False,
        error_messages=generate_error_messages("birthday")
    )

    location = serializers.CharField(
        allow_null=False,
        allow_blank=True,
        required=False,
        max_length=250,
        error_messages=generate_error_messages("location")
    )

    theme = serializers.CharField(
        required=False,
        allow_null=False,
        allow_blank=True,
        max_length=250,
        error_messages=generate_error_messages("theme")
    )

    contacts = UpdateContactsSerializer(
        required=False,
        allow_null=False,
        error_messages=generate_error_messages("contacts")
    )

    def update(self, instance, validated_data):
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.about_me = validated_data.get("aboutMe", instance.about_me)
        instance.status = validated_data.get("status", instance.status)
        instance.location = validated_data.get("location", instance.location)
        instance.birthday = validated_data.get("birthday", instance.birthday)
        instance.theme = validated_data.get("theme", instance.theme)
        instance.is_looking_for_a_job = validated_data.get(
            "isLookingForAJob", instance.is_looking_for_a_job)
        instance.professional_skills = validated_data.get(
            "professionalSkills", instance.professional_skills)

        if "contacts" in validated_data:
            contacts_data = validated_data.pop("contacts")
            contacts = instance.contacts

            contacts.github = contacts_data.get("github", contacts.github)
            contacts.vk = contacts_data.get("vk", contacts.vk)
            contacts.facebook = contacts_data.get(
                "facebook", contacts.facebook)
            contacts.instagram = contacts_data.get(
                "instagram", contacts.instagram)
            contacts.twitter = contacts_data.get("twitter", contacts.twitter)
            contacts.website = contacts_data.get("website", contacts.website)
            contacts.youtube = contacts_data.get("youtube", contacts.youtube)
            contacts.main_link = contacts_data.get(
                "mainLink", contacts.main_link)

            contacts.save()

        instance.save()
        return instance


class UpdatePasswordSerailizer(serializers.Serializer):
    oldPassword, newPassword1, newPassword2 = [
        serializers.CharField(
            max_length=128,
            required=True,
            allow_blank=False,
            allow_null=False,
            error_messages=generate_error_messages(i)) for i in [
            "old password", "new password", "repeat new password"
        ]
    ]

    def validate(self, data):
        request = self.context["request"]

        if not request.user.check_password(data["oldPassword"]):
            raise serializers.ValidationError({
                "oldPassword": "Invalid password"
            })

        if data["newPassword1"] != data["newPassword2"]:
            raise serializers.ValidationError({
                "newPassword2": "Passwords do not match"
            })

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data["newPassword1"])
        instance.save()

        return instance
