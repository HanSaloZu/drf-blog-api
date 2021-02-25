from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    login = models.CharField("login", db_index=True,
                             unique=True, max_length=160)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["login"]

    objects = UserManager()

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "users"
