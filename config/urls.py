from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/profile/", include("profiles.urls")),
    path("api/v1/followers/", include("followers.followers_urls")),
    path("api/v1/following/", include("followers.following_urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/posts/", include("posts.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
