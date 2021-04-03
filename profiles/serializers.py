from rest_framework import serializers

from .models import Profile, Photos, Contacts


class PhotosSerializer(serializers.ModelSerializer):
    small, large = [serializers.ImageField(
        required=False, allow_null=False, error_messages={
            "invalid": "Choose Image file",
            "null": "Choose Image file"
        }) for i in range(2)]

    class Meta:
        model = Photos
        fields = ["small", "large"]


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
    lookingForAJob = serializers.SerializerMethodField()
    lookingForAJobDescription = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()
    aboutMe = serializers.SerializerMethodField()
    contacts = ContactsSerializer()
    photos = PhotosSerializer()

    def get_userId(self, obj):
        return obj.user.id

    def get_lookingForAJob(self, obj):
        return obj.looking_for_a_job

    def get_lookingForAJobDescription(self, obj):
        return obj.looking_for_a_job_description

    def get_fullName(self, obj):
        return obj.fullname

    def get_aboutMe(self, obj):
        return obj.about_me

    class Meta:
        model = Profile
        fields = ["userId", "lookingForAJob",
                  "lookingForAJobDescription", "fullName", "contacts", "aboutMe", "photos"]


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
        required=True, allow_null=False, error_messages=get_error_messages("lookingForAJob", "string"))

    LookingForAJobDescription = serializers.CharField(
        required=True, allow_blank=False, allow_null=False, error_messages=get_error_messages("LookingForAJobDescription", "string"))

    fullName = serializers.CharField(
        max_length=300, required=True, allow_blank=False,
        allow_null=False, error_messages=get_error_messages("FullName", "string"))

    aboutMe = serializers.CharField(
        max_length=300, required=True, allow_blank=False, allow_null=False, error_messages=get_error_messages("AboutMe", "string"))

    contacts = UpdateContactsSerializer(
        default=UpdateContactsSerializer(), required=False, allow_null=True)


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, max_length=300, allow_null=False, allow_blank=True, error_messages={
        "max_length": "Max Status length is 300 symbols"
    })

    class Meta:
        model = Profile
        fields = ["status"]
