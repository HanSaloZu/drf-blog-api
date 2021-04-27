from django.urls import path

from .views import (ProfileStatusDetail, ProfileDetail,
                    ProfileStatusUpdate, ProfilePhotoUpdate, ProfileUpdate)

urlpatterns = [
    path("", ProfileUpdate.as_view(), name="profile_update"),
    path("status/<int:user_id>/", ProfileStatusDetail.as_view(),
         name="profile_status_detail"),
    path("status/", ProfileStatusUpdate.as_view(), name="profile_status_update"),
    path("<int:user_id>/", ProfileDetail.as_view(), name="profile_detail"),
    path("photo/", ProfilePhotoUpdate.as_view(), name="profile_photo_update")
]
