from django.urls import path

from .views import Follow

urlpatterns = [
    path("<int:user_id>/", Follow.as_view(), name="follow")
]
