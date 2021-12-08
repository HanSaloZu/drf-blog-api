from django.contrib.auth import get_user_model
from django.db import Error, models

User = get_user_model()


class Follower(models.Model):
    follower_user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("follower_user", "following_user")
        verbose_name = "follower"
        db_table = "followers"

    def __str__(self):
        return f"{self.follower_user} followed {self.following_user}"

    def save(self, *args, **kwargs):
        if self.follower_user == self.following_user:
            raise Error(
                "Attempted to create a follow object where follower_user == following_user")
        super(Follower, self).save(*args, **kwargs)
