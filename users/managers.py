from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, login, password, **extra_fileds):
        if not email:
            raise ValueError("Please enter your Email")

        email = self.normalize_email(email)
        user = self.model(email=email, login=login, **extra_fileds)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, login, password, **extra_fileds):
        extra_fileds.setdefault("is_superuser", False)
        return self._create_user(email, login, password, **extra_fileds)

    def create_superuser(self, email, login, password, **extra_fileds):
        extra_fileds.setdefault("is_superuser", True)

        if extra_fileds.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, login, password, **extra_fileds)
