from django.urls import path

from .views import (ListLikedPostsAPIView, ListPostsAPIView,
                    RetrieveCreateDestroyLikedPostAPIView,
                    RetrieveUpdateProfileAPIView, UpdateAvatarAPIView,
                    UpdateBannerAPIView, UpdatePasswordAPIView)

urlpatterns = [
    path("", RetrieveUpdateProfileAPIView.as_view(), name="profile"),
    path("avatar/", UpdateAvatarAPIView.as_view(),
         name="profile_avatar_update"),
    path("banner/", UpdateBannerAPIView.as_view(),
         name="profile_banner_update"),
    path("password/", UpdatePasswordAPIView.as_view(), name="update_password"),
    path("posts/", ListPostsAPIView.as_view(), name="posts_list"),
    path("liked/", ListLikedPostsAPIView.as_view(),
         name="liked_posts_list"),
    path("liked/<int:id>/",
         RetrieveCreateDestroyLikedPostAPIView.as_view(),
         name="liked_posts")
]
