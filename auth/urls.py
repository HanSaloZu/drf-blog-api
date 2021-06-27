from django.urls import path

from .views import UserAuthentication

urlpatterns = [
    path("", UserAuthentication.as_view(), name="authentication")
]
