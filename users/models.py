from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    login = models.CharField(db_index=True,
                             unique=True, max_length=160)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["login"]

    objects = UserManager()

    def __str__(self):
        return self.login

    class Meta:
        verbose_name = "user"
        db_table = "users"
        ordering = ["-id"]
