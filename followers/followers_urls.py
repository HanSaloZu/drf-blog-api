from django.urls import path

from .views import FollowersListAPIView

urlpatterns = [
    path("", FollowersListAPIView.as_view(), name="followers_list")
]
