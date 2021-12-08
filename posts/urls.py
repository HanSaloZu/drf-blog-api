from django.urls import path

from .views import ListCreatePostAPIView, RetrieveUpdateDestroyPostAPIView

urlpatterns = [
    path("", ListCreatePostAPIView.as_view(), name="list_create_post"),
    path("<int:id>/", RetrieveUpdateDestroyPostAPIView.as_view(), name="post")
]
