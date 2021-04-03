from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)

    looking_for_a_job = models.BooleanField(default=False)
    looking_for_a_job_description = models.TextField(default=None, null=True)

    fullname = models.CharField(max_length=300)
    status = models.CharField(
        default="", max_length=300, blank=True, null=False)
    about_me = models.TextField(default=None, null=True)

    def __str__(self):
        return f"{self.user.login} profile"

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profiles"


class Photos(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, unique=True)
    small = models.ImageField(
        "small photo", default=None, upload_to="photos/small", null=True)
    large = models.ImageField(
        "large photo", default=None, upload_to="photos/large", null=True)

    def __str__(self):
        return f"{self.profile.user.login} photos"

    def save(self, *args, **kwargs):
        super().save()
        if (self.small and self.large):
            photos_data = [
                {"size": (100, 100), "path": self.small.path},  # small photo
                {"size": (300, 300), "path": self.large.path}]  # large photo

            for current_photo in photos_data:
                photo = Image.open(current_photo["path"])
                resized_photo = photo.resize(current_photo["size"])
                resized_photo.save(current_photo["path"],
                                   quality="web_maximum", subsampling=0)

    class Meta:
        verbose_name = "profile photos"
        verbose_name_plural = "profiles photos"
        db_table = "profile_photos"


class Contacts(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, unique=True)
    facebook, github, instagram, main_link, twitter, vk, website, youtube = [models.CharField(
        max_length=300, null=True, blank=True) for i in range(8)]

    def __str__(self):
        return f"{self.profile.user.login} contacts"

    class Meta:
        verbose_name = "user contacts"
        verbose_name_plural = "users contacts"
        db_table = "user_contacts"
