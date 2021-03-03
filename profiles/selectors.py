from .models import Profile


def get_profile_by_user_id(user_id):
    return Profile.objects.get(user=user_id)
