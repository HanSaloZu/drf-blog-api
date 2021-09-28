from django.urls import path

from .views import (ListCreateUsersAPIView, ListUserFollowersAPIView,
                    ListUserFollowingAPIView, ListUserPostsAPIView,
                    RetrieveUserProfileAPIView)

urlpatterns = [
    path("", ListCreateUsersAPIView.as_view(), name="users_list"),
    path("<str:login>/", RetrieveUserProfileAPIView.as_view(),
         name="user_profile_detail"),
    path("<str:login>/posts/", ListUserPostsAPIView.as_view(),
         name="user_posts_list"),
    path("<str:login>/followers/", ListUserFollowersAPIView.as_view(),
         name="user_followers_list"),
    path("<str:login>/following/", ListUserFollowingAPIView.as_view(),
         name="user_following_list")
]
