from rest_framework import serializers

from .models import Profile, Contacts, ProfilePreferences


class ContactsSerializer(serializers.ModelSerializer):
    mainLink = serializers.SerializerMethodField()

    def get_mainLink(self, obj):
        return obj.main_link

    class Meta:
        model = Contacts
        fields = ["github", "vk", "facebook",
                  "instagram", "twitter", "website", "youtube", "mainLink"]


class ProfileSerializer(serializers.ModelSerializer):
    userId = serializers.SerializerMethodField()
    login = serializers.SerializerMethodField()
    isLookingForAJob = serializers.SerializerMethodField()
    professionalSkills = serializers.SerializerMethodField()
    aboutMe = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    contacts = ContactsSerializer()

    def get_userId(self, obj):
        return obj.user.id

    def get_login(self, obj):
        return obj.user.login

    def get_isLookingForAJob(self, obj):
        return obj.is_looking_for_a_job

    def get_professionalSkills(self, obj):
        return obj.professional_skills

    def get_aboutMe(self, obj):
        return obj.about_me

    def get_photo(self, obj):
        return obj.photo.link

    class Meta:
        model = Profile
        fields = ["userId", "isLookingForAJob",
                  "professionalSkills", "fullname", "login", "status", "aboutMe", "photo", "contacts"]


def get_error_messages(field_name):
    capitalized_field_name = field_name.capitalize()

    return {
        "required": f"{capitalized_field_name} field is required",
        "null": f"{capitalized_field_name} field cannot be null",
        "blank": f"{capitalized_field_name} field cannot be empty",
        "invalid": f"Invalid value for {field_name} field",
        "max_length": f"{capitalized_field_name} field value is too long",
        "min_length": f"{capitalized_field_name} field value is too short",
    }


class UpdateContactsSerializer(serializers.Serializer):
    github, vk, facebook, instagram, twitter, website, youtube, mainLink = [
        serializers.URLField(
            max_length=200,
            required=False,
            allow_blank=True,
            error_messages=get_error_messages(i)) for i in [
            "github", "vk", "facebook", "instagram", "twitter", "website", "youtube", "mainLink"
        ]
    ]


class UpdateProfileSerializer(serializers.Serializer):
    isLookingForAJob = serializers.BooleanField(
        allow_null=False,
        error_messages=get_error_messages("is looking for a job")
    )

    professionalSkills = serializers.CharField(
        allow_blank=True,
        max_length=350,
        allow_null=False,
        error_messages=get_error_messages("professional skills")
    )

    fullname = serializers.CharField(
        max_length=150,
        allow_blank=False,
        allow_null=False,
        error_messages=get_error_messages("fullname")
    )

    status = serializers.CharField(
        max_length=70,
        allow_null=False,
        allow_blank=True,
        error_messages=get_error_messages("status")
    )

    aboutMe = serializers.CharField(
        max_length=400,
        allow_blank=False,
        allow_null=False,
        min_length=70,
        error_messages=get_error_messages("about me")
    )

    contacts = UpdateContactsSerializer(
        required=False,
        allow_null=False,
        error_messages=get_error_messages("contacts")
    )

    def update(self, instance, validated_data):
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.about_me = validated_data.get("aboutMe", instance.about_me)
        instance.status = validated_data.get("status", instance.status)
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


class ProfilePreferencesSerializer(serializers.ModelSerializer):
    theme = serializers.CharField(required=True, allow_null=False, allow_blank=False,
                                  max_length=255, error_messages={
                                      "required": "Theme field is required",
                                      "max_length": "Theme field max length is 255 symbols",
                                      "null": "Theme value cannot be null",
                                      "blank": "Theme value cannot be empty"})

    class Meta:
        model = ProfilePreferences
        fields = ["theme"]
