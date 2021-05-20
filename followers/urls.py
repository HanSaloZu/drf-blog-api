from django.urls import path

from .views import FollowAPIView

urlpatterns = [
    path("<int:user_id>/", FollowAPIView.as_view(), name="follow")
]
