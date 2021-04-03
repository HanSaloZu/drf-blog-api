from django.urls import path

from .views import follow

urlpatterns = [
    path("/<int:user_id>", follow, name="follow")
]
