from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile, Contacts, Photos

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance, fullname=instance.login)
        profile.save()
        contacts = Contacts(profile=profile)
        contacts.save()
        photos = Photos(profile=profile)
        photos.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.profile.contacts.save()
    instance.profile.photos.save()