from django.urls import path

from .views import AuthenticationAPIView, ProfileActivationAPIView

urlpatterns = [
    path("", AuthenticationAPIView.as_view(), name="authentication"),
    path("activation/", ProfileActivationAPIView.as_view(),
         name="profile_activation")
]
