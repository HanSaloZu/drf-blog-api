from django.urls import path

from .views import user_detail, user_authentication

urlpatterns = [
    path("me/", user_detail, name="user_detail"),
    path("login/", user_authentication, name="authentication")
]
