from django.db import models
from django.contrib.auth import get_user_model
from django.db import models, Error

User = get_user_model()


class VerificationCode(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "verification_code"
        verbose_name_plural = "verification_codes"
        db_table = "verification_codes"

    def __str__(self):
        return f"{self.user.login} verification code"

    def save(self, *args, **kwargs):
        if self.user.is_active:
            raise Error(
                "Attempted to create a verification code for active user")

        return super(VerificationCode, self).save(*args, **kwargs)
