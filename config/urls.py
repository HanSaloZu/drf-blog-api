from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/1.0/auth/", include("users.auth_urls")),
    path("api/1.0/profile/", include("profiles.urls")),
    path("api/1.0/follow/", include("following.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
