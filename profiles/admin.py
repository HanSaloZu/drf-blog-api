from django.contrib import admin

from .models import Profile, Photo, Contacts, ProfilePreferences


class NoAddPermissionAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(Profile)
class ProfileAdmin(NoAddPermissionAdminModel):
    list_display = ("user", "fullname", "looking_for_a_job", "status")
    list_display_links = ("user", "fullname", "looking_for_a_job")
    list_filter = ("looking_for_a_job",)
    search_fields = ("user__login", "fullname")
    fieldsets = (
        (None, {
            "fields": ("fullname", "status", "about_me")
        }),
        ("Job", {
            "fields": ("looking_for_a_job", "looking_for_a_job_description")
        })
    )


@admin.register(Photo)
class PhotosAdmin(NoAddPermissionAdminModel):
    list_display = ("profile", "file_id", "link")
    list_display_links = ("profile", "file_id", "link")
    search_fields = ("profile__user__login",
                     "profile__user__email", "profile__fullname")
    fields = ("file_id", "link")

    def has_change_permission(self, request):
        return False


@admin.register(Contacts)
class ContactsAdmin(NoAddPermissionAdminModel):
    list_display = ("profile", "facebook", "github", "instagram",
                    "main_link", "twitter", "vk", "website", "youtube")
    list_display_links = ("profile", "facebook", "github", "instagram",
                          "main_link", "twitter", "vk", "website", "youtube")
    search_fields = ("profile__user__login",
                     "profile__user__email", "profile__fullname")
    fields = ("facebook", "github", "instagram",
              "main_link", "twitter", "vk", "website", "youtube")


@admin.register(ProfilePreferences)
class ProfilesPreferencesAdmin(NoAddPermissionAdminModel):
    list_display = ("profile", "theme")
    list_display_links = ("profile", "theme")
    search_fields = ("profile__user__login",
                     "profile__user__email", "profile__fullname")
    list_filter = ("theme",)
    fields = ("theme",)
