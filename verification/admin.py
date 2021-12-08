from django.contrib import admin

from utils.admin import NoAddPermissionAdminModel, NoChangePermissionAdminModel

from .models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(NoAddPermissionAdminModel,
                            NoChangePermissionAdminModel):
    list_display = ("user", "code", "created_at")
    list_display_links = ("user", "code")
    search_fields = ("user__login", "code")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {
            "fields": ("user", "code", "created_at")
        }),
    )
