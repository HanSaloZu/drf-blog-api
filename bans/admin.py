from django.contrib import admin

from .models import Ban


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ("receiver", "reason", "creator", "banned_at")
    list_display_links = ("receiver", "banned_at")
    search_fields = ("receiver__login", "creator__login", "reason")
    readonly_fields = ("banned_at",)
