from django.urls import path

from .views import profile_status_detail

urlpatterns = [
    path("status/<int:user_id>", profile_status_detail,
         name="profile_status_detail")
]
