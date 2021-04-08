from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "login", "is_staff", "is_superuser")
    list_display_links = ("id", "email", "login")
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("id", "email", "login")
    fieldsets = (
        ("Common data", {
            "fields": ("email", "login", "password")
        }),
        ("Advanced options", {
            "fields": ("is_staff", "is_superuser")
        })
    )
