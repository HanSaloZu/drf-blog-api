from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    login = models.SlugField(db_index=True,
                             unique=True, max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("login",)

    objects = UserManager()

    class Meta:
        verbose_name = "user"
        db_table = "users"
        ordering = ("-id",)

    def __str__(self):
        return self.login
