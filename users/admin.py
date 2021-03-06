from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("id", "email", "login", "is_staff",
                    "is_superuser", "is_active")
    list_display_links = ("id", "email", "login")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("id", "email", "login")
    fieldsets = (
        ("Common data", {
            "fields": ("email", "login", "password")
        }),
        ("Advanced options", {
            "fields": ("is_staff", "is_superuser", "is_active")
        })
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "login", "password1",
                       "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )
    ordering = ("-id",)
