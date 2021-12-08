from django.urls import path

from .views import FollowingAPIView, FollowingListAPIView

urlpatterns = [
    path("", FollowingListAPIView.as_view(), name="following_list"),
    path("<str:login>/", FollowingAPIView.as_view(), name="following")
]
