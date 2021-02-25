from django.test import TestCase
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()

    def _create_user(self, login, email, password, is_superuser):
        if is_superuser:
            return self.UserModel.objects.create_superuser(
                login=login, email=email, password=password, is_superuser=True)

        return self.UserModel.objects.create_user(
            login=login, email=email, password=password)
