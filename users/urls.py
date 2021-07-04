from django.urls import path

from .views import UsersList, RetrieveUserProfileAPIView

urlpatterns = [
    path("", UsersList.as_view(), name="users_list"),
    path("<str:login>/profile", RetrieveUserProfileAPIView.as_view(),
         name="user_profile_detail"),
]
