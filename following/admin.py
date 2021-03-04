from django.contrib import admin

from .models import FollowersModel


@admin.register(FollowersModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("follower_user", "following_user")
    list_display_links = ("follower_user", "following_user")
    list_filter = ("follower_user", "following_user")
    search_fields = ("follower_user", "following_user")
