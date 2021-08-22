from django.contrib import admin

from .models import Follower


@admin.register(Follower)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("follower_user", "following_user")
    list_display_links = ("follower_user", "following_user")
    search_fields = ("follower_user__login", "follower_user__email",
                     "following_user__login", "following_user__email")
