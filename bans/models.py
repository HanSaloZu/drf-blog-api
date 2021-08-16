from django.db import models, Error
from django.contrib.auth import get_user_model

User = get_user_model()


class Ban(models.Model):
    receiver = models.OneToOneField(
        User, related_name="ban", on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, related_name="ban_creator", on_delete=models.CASCADE)

    reason = models.CharField(max_length=250, blank=True)
    banned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ban"
        verbose_name_plural = "bans"
        db_table = "bans"

    def __str__(self):
        return f"{self.receiver.login} banned by {self.creator.login}"

    def save(self, *args, **kwargs):
        if self.receiver == self.creator:
            raise Error("Self-banning is prohibited")
        if not self.creator.is_staff:
            raise Error("Bans can only be created by admins")
        if self.receiver.is_staff:
            raise Error("Admins cannot be banned")

        super(Ban, self).save(*args, **kwargs)
