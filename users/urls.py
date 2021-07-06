from django.urls import path

from .views import (UsersListAPIView, RetrieveUserProfileAPIView,
                    UserFollowersListAPIView)

urlpatterns = [
    path("", UsersListAPIView.as_view(), name="users_list"),
    path("<str:login>/profile", RetrieveUserProfileAPIView.as_view(),
         name="user_profile_detail"),
    path("<str:login>/followers", UserFollowersListAPIView.as_view(),
         name="user_followers_list")
]
