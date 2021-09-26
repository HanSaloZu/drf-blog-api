from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/token/", include("authentication.urls")),
    path("api/v1/profile/", include("profiles.urls")),
    path("api/v1/profile/followers/", include("followers.followers_urls")),
    path("api/v1/profile/following/", include("followers.following_urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/posts/", include("posts.urls")),
    path("api/v1/news/", include("news.urls")),
    path("api/v1/bans/", include("bans.urls")),
    path("api/v1/verification/", include("verification.urls"))
]
