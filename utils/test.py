from django.test import TestCase
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()

    def _create_user(self, login, email, password, is_superuser):
        self.UserModel.objects.create(
            login=login, email=email, password=password, is_superuser=is_superuser)
