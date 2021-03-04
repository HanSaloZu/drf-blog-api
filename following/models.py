from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowersModel(models.Model):
    follower_user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["follower_user", "following_user"]
        verbose_name = "follower"
        db_table = "followers"
