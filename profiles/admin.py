from django.contrib import admin

from .models import Profile, Avatar, Contacts, Banner


class NoAddPermissionAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class NoChangePermissionAdminModel(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Profile)
class ProfileAdmin(NoAddPermissionAdminModel):
    list_display = ("user", "fullname", "is_looking_for_a_job", "birthday")
    list_display_links = ("user", "fullname", "is_looking_for_a_job")
    list_filter = ("is_looking_for_a_job",)
    search_fields = ("user__login", "fullname")
    fieldsets = (
        (None, {
            "fields": ("fullname", "status", "about_me", "location",
                       "birthday")
        }),
        ("Job", {
            "fields": ("is_looking_for_a_job", "professional_skills")
        })
    )


@admin.register(Avatar)
class AvatarsAdmin(NoAddPermissionAdminModel, NoChangePermissionAdminModel):
    list_display = ("profile", "link")
    list_display_links = ("profile", "link")
    search_fields = ("profile__user__login",
                     "profile__user__email", "profile__fullname")
    fields = ("file_id", "link")


@admin.register(Banner)
class BannersAdmin(NoAddPermissionAdminModel, NoChangePermissionAdminModel):
    list_display = ("profile", "link")
    list_display_links = ("profile", "link")
    search_fields = ("profile__user__login",
                     "profile__user__email", "profile__fullname")
    fields = ("file_id", "link")


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
