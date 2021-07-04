from .models import Profile, Contacts


def get_profile_by_user_id(user_id):
    return Profile.objects.get(user=user_id)


def get_contacts_by_user_id(user_id):
    return Contacts.objects.filter(profile=get_profile_by_user_id(user_id))


def get_profile_by_user_login(user_login):
    return Profile.objects.get(user__login=user_login)
