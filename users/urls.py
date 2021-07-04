from django.urls import path

from .views import UsersListAPIView, RetrieveUserProfileAPIView

urlpatterns = [
    path("", UsersListAPIView.as_view(), name="users_list"),
    path("<str:login>/profile", RetrieveUserProfileAPIView.as_view(),
         name="user_profile_detail"),
]
