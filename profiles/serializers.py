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


class UpdateContactsSerializer(serializers.Serializer):
    github, vk, facebook, instagram, twitter, website, youtube, mainLink = [serializers.URLField(
        max_length=300, default=None, required=False, allow_blank=True, allow_null=True) for i in range(8)]


def get_error_messages(field_name, data_type):
    res = dict.fromkeys(["null", "required", "blank"],
                        f"The {field_name} field is required. ({field_name})")
    res.update(
        {"invalid": f"Invalid {data_type}. ({field_name})"})
    return res


class UpdateProfileSerializer(serializers.Serializer):
    lookingForAJob = serializers.BooleanField(
        required=False, allow_null=False, error_messages=get_error_messages("lookingForAJob", "boolean"))

    lookingForAJobDescription = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)

    fullName = serializers.CharField(
        max_length=300, required=True, allow_blank=False,
        allow_null=False, error_messages=get_error_messages("FullName", "string"))

    aboutMe = serializers.CharField(
        max_length=300, required=True, allow_blank=False, allow_null=False, error_messages=get_error_messages("AboutMe", "string"))

    contacts = UpdateContactsSerializer(
        default=UpdateContactsSerializer(), required=False, allow_null=True)


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
