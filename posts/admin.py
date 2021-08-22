from django.contrib import admin

from utils.admin import NoChangePermissionAdminModel, NoAddPermissionAdminModel

from .models import Post, Like, Attachment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "created_at")
    list_display_links = ("id", "author", "title")
    search_fields = ("id", "author__login", "title")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {
            "fields": ("author", "title", "body", "created_at", "updated_at")
        }),
    )
    ordering = ("-created_at",)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post")
    list_display_links = ("user", "post")
    search_fields = ("user__login", "post__id", "post__title")


@admin.register(Attachment)
class AttachmentAdmin(NoAddPermissionAdminModel, NoChangePermissionAdminModel):
    list_display = ("post", "link")
    list_display_links = ("post",)
    search_fields = ("post__title", "post__body", "post__author__login")
