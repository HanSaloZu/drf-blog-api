from django.urls import path

from .views import FollowingAPIView

urlpatterns = [
    path("<str:login>", FollowingAPIView.as_view(), name="following")
]
