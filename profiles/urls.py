from django.urls import path

from .views import (ProfileDetail, ProfileStatusUpdate, ProfilePhotoUpdate,
                    ProfileUpdate, ProfilePreferences)

urlpatterns = [
    path("", ProfileUpdate.as_view(), name="profile_update"),
    path("<int:pk>/", ProfileDetail.as_view(), name="profile_detail"),
    path("photo/", ProfilePhotoUpdate.as_view(), name="profile_photo_update"),
    path("preferences/", ProfilePreferences.as_view(), name="profile_preferences")
]
