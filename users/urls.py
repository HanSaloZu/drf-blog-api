from django.urls import path

from .views import user_detail, user_authentication

urlpatterns = [
    path("auth/me", user_detail, name="user_detail"),
    path("auth/login", user_authentication, name="authentication")
]
