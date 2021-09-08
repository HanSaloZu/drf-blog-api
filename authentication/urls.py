from django.urls import path

from .views import CustomObtainTokenPairAPIView, CustomTokenRefreshAPIView


urlpatterns = [
    path("", CustomObtainTokenPairAPIView.as_view(), name="token_create"),
    path("refresh/", CustomTokenRefreshAPIView.as_view(), name="token_refresh")
]
