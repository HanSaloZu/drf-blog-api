from django.urls import path

from .views import (ListUsersAPIView, RetrieveUserProfileAPIView,
                    ListUserFollowersAPIView, ListUserFollowingAPIView)

urlpatterns = [
    path("", ListUsersAPIView.as_view(), name="users_list"),
    path("<str:login>/", RetrieveUserProfileAPIView.as_view(),
         name="user_profile_detail"),
    path("<str:login>/followers/", ListUserFollowersAPIView.as_view(),
         name="user_followers_list"),
    path("<str:login>/following/", ListUserFollowingAPIView.as_view(),
         name="user_following_list")
]
