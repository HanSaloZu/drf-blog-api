from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)

    is_looking_for_a_job = models.BooleanField(default=False)
    professional_skills = models.TextField(blank=True)

    fullname = models.CharField(max_length=50)
    status = models.CharField(max_length=70, blank=True)
    about_me = models.TextField(blank=True)
    location = models.CharField(max_length=250, blank=True)
    birthday = models.DateField(null=True)
    theme = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profiles"

    def __str__(self):
        return f"{self.user.login} profile"


class ProfileRelatedModel(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, unique=True)

    class Meta:
        abstract = True


class ImageModel(ProfileRelatedModel):
    file_id = models.CharField(max_length=50, blank=True)
    link = models.URLField(max_length=300, blank=True)

    class Meta:
        abstract = True


class Avatar(ImageModel):
    class Meta:
        verbose_name = "profile avatar"
        verbose_name_plural = "profiles avatars"
        db_table = "profiles_avatars"

    def __str__(self):
        return f"{self.profile.user.login} avatar"


class Banner(ImageModel):
    class Meta:
        verbose_name = "profile banner"
        verbose_name_plural = "profiles banners"
        db_table = "profiles_banners"

    def __str__(self):
        return f"{self.profile.user.login} banner"


class Contacts(ProfileRelatedModel):
    facebook, github, instagram, main_link, twitter, vk, website, youtube = [
        models.URLField(blank=True) for i in range(8)
    ]

    class Meta:
        verbose_name = "user contacts"
        verbose_name_plural = "users contacts"
        db_table = "users_contacts"

    def __str__(self):
        return f"{self.profile.user.login} contacts"
