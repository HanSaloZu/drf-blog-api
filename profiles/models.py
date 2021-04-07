from django.db import models
from django.contrib.auth import get_user_model

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

    photo = models.URLField(default=None, max_length=300, null=True)

    def __str__(self):
        return f"{self.user.login} profile"

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"
        db_table = "profiles"


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
