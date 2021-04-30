from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FollowersModel(models.Model):
    follower_user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE)

    @classmethod
    def follow(self, user, subject):
        pair = self.objects.create(follower_user=user, following_user=subject)
        pair.save()
        return pair

    @classmethod
    def unfollow(self, user, subject):
        self.objects.filter(follower_user=user,
                            following_user=subject).delete()

    @classmethod
    def is_following(self, user, subject):
        return self.objects.filter(follower_user=user, following_user=subject).exists()

    class Meta:
        unique_together = ["follower_user", "following_user"]
        verbose_name = "follower"
        db_table = "followers"
