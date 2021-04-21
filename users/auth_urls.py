from django.urls import path

from .views import UserDetail, user_authentication

urlpatterns = [
    path("me/", UserDetail.as_view(), name="user_detail"),
    path("login/", user_authentication, name="authentication")
]
