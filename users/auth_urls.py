from django.urls import path

from .views import UserDetail, UserAuthentication

urlpatterns = [
    path("me/", UserDetail.as_view(), name="user_detail"),
    path("login/", UserAuthentication.as_view(), name="authentication")
]
