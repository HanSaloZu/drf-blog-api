from django.urls import path

from .views import CustomObtainTokenPairAPIView


urlpatterns = [
    path("", CustomObtainTokenPairAPIView.as_view(), name="token_create")
]
