from django.urls import path

from .views import user_detail

urlpatterns = [
    path("auth/me", user_detail, name="user_detail")
]
