from django.urls import path

from .views import EmailVerificationAPIView

urlpatterns = [
    path("", EmailVerificationAPIView.as_view(), name="verification")
]
