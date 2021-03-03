from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/1.0/auth/", include("users.urls")),
    path("api/1.0/profile/", include("profiles.urls"))
]
