from django.urls import path

from .views import (RetrieveUpdateProfileAPIView,
                    UpdatePhotoAPIView, RetrieveUpdatePreferencesAPIView)

urlpatterns = [
    path("", RetrieveUpdateProfileAPIView.as_view(), name="profile"),
    path("photo/", UpdatePhotoAPIView.as_view(), name="profile_photo_update"),
    path("preferences/", RetrieveUpdatePreferencesAPIView.as_view(),
         name="profile_preferences")
]
