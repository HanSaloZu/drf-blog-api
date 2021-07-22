from django.urls import path

from .views import (RetrieveUpdateProfileAPIView, UpdatePasswordAPIView,
                    UpdateAvatarAPIView, RetrieveUpdatePreferencesAPIView, UpdateBannerAPIView)

urlpatterns = [
    path("", RetrieveUpdateProfileAPIView.as_view(), name="profile"),
    path("avatar/", UpdateAvatarAPIView.as_view(), name="profile_avatar_update"),
    path("banner/", UpdateBannerAPIView.as_view(), name="profile_banner_update"),
    path("preferences/", RetrieveUpdatePreferencesAPIView.as_view(),
         name="profile_preferences"),
    path("password/", UpdatePasswordAPIView.as_view(), name="update_password")
]
