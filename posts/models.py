from django.contrib.auth import get_user_model
from django.db import Error, models

from profiles.models import ImageModel

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        db_table = "posts"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Post #{self.id}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "post")
        verbose_name = "like"
        verbose_name_plural = "likes"
        db_table = "likes"

    def __str__(self):
        return f"{self.user.login} liked post #{self.post.id}"


class Attachment(ImageModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        attachments_count = Attachment.objects.all().filter(
            post=self.post
        ).count()

        if attachments_count >= 5:
            raise Error("Maximum 5 attachments per post")

        super(Attachment, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "attachment"
        verbose_name_plural = "attachments"
        db_table = "attachments"

    def __str__(self):
        return f"Attachment to post #{self.post.id}"
