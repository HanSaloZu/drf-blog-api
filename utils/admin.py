from django.contrib import admin


class NoAddPermissionAdminModel(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


class NoChangePermissionAdminModel(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class NoDeletePermissionAdminModel(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
