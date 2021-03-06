from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Avatar, Banner, Contacts, Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance, fullname=instance.login)
        profile.save()

        Contacts(profile=profile).save()
        Avatar(profile=profile).save()
        Banner(profile=profile).save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.contacts.save()
    instance.profile.avatar.save()
    instance.profile.banner.save()
