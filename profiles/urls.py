from django.urls import path

from .views import (profile_status_detail, profile_detail,
                    profile_status_update, profile_photo_update, profile_update)

urlpatterns = [
    path("", profile_update, name="profile_update"),
    path("status/<int:user_id>/", profile_status_detail,
         name="profile_status_detail"),
    path("status/", profile_status_update, name="profile_status_update"),
    path("<int:user_id>/", profile_detail, name="profile_detail"),
    path("photo/", profile_photo_update, name="profile_photo_update")
]
