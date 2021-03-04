from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_by_id(id):
    return User.objects.get(id=id)
