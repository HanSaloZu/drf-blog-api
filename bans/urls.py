from django.urls import path

from .views import ListBannedUsersAPIView


urlpatterns = [
    path("", ListBannedUsersAPIView.as_view(), name="bans_list")
]
