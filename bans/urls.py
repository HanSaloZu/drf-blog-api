from django.urls import path

from .views import ListBannedUsersAPIView, BanAPIView


urlpatterns = [
    path("", ListBannedUsersAPIView.as_view(), name="bans_list"),
    path("<str:login>/", BanAPIView.as_view(), name="ban")
]
