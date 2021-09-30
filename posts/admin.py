from django.contrib import admin

from utils.admin import NoAddPermissionAdminModel, NoChangePermissionAdminModel

from .models import Attachment, Like, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")
    list_display_links = ("id", "author")
    search_fields = ("id", "author__login", "body")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("author", "body", "created_at", "updated_at")
        }),
    )
    ordering = ("-created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post")
    list_display_links = ("user", "post")
    search_fields = ("user__login", "post__id")


@admin.register(Attachment)
class AttachmentAdmin(NoAddPermissionAdminModel, NoChangePermissionAdminModel):
    list_display = ("post", "link")
    list_display_links = ("post",)
    search_fields = ("post__body", "post__author__login")
