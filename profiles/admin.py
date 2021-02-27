from django.contrib import admin

from .models import Profile, Photos, Contacts


class NoAddPermissionAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(Profile)
class ProfileAdmin(NoAddPermissionAdminModel):
    list_display = ("user", "fullname", "looking_for_a_job", "status")
    list_display_links = ("user", "fullname", "looking_for_a_job")
    list_filter = ("looking_for_a_job",)
    search_fields = ("user", "fullname")
    fieldsets = (
        (None, {
            "fields": ("fullname", "status", "about_me")
        }),
        ("Job", {
            "fields": ("looking_for_a_job", "looking_for_a_job_description")
        })
    )


@admin.register(Photos)
class PhotosAdmin(NoAddPermissionAdminModel):
    list_display = ("profile", "small", "large")
    list_display_links = ("profile", "small", "large")
    search_fields = ("profile",)
    fields = ("small", "large")


@admin.register(Contacts)
class ContactsAdmin(NoAddPermissionAdminModel):
    list_display = ("profile", "facebook", "github", "instagram",
                    "main_link", "twitter", "vk", "website", "youtube")
    list_display_links = ("profile", "facebook", "github", "instagram",
                          "main_link", "twitter", "vk", "website", "youtube")
    search_fields = ("profile",)
    fields = ("facebook", "github", "instagram",
              "main_link", "twitter", "vk", "website", "youtube")
