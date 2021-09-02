from django.urls import path

from .views import AuthenticationAPIView

urlpatterns = [
    path("", AuthenticationAPIView.as_view(), name="authentication")
]
