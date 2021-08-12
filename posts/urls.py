from django.urls import path

from .views import RetrieveUpdateDestroyPostAPIView

urlpatterns = [
    path("<int:id>/", RetrieveUpdateDestroyPostAPIView.as_view(), name="post")
]
