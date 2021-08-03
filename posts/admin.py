from django.contrib import admin

from .models import Post


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
