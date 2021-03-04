from .models import User


def get_all_users():
    return User.objects.all()


def get_users_by_term(term):
    return User.objects.filter(login__contains=term)
