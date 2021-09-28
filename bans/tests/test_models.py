from django.db import Error, IntegrityError, transaction

from utils.tests import ExtendedTestCase

from ..models import Ban
from ..services import ban_user


class BanModelTestCase(ExtendedTestCase):
    model = Ban

    def setUp(self):
        self.admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")
        self.second_admin = self.UserModel.objects.create_superuser(
            login="SecondAdmin", email="2admin@gmail.com", password="pass")
        self.user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")

    def test_ban(self):
        ban_user(receiver=self.user, creator=self.admin, reason="Ban")
        ban_object = self.model.objects.all().first()

        self.assertIsInstance(ban_object, Ban)
        self.assertEqual(ban_object.receiver, self.user)
        self.assertEqual(ban_object.creator, self.admin)
        self.assertEqual(ban_object.reason, "Ban")

    def test_double_ban(self):
        """
        Double ban should raise an IntegrityError
        """

        ban_user(receiver=self.user, creator=self.admin)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ban_user(receiver=self.user, creator=self.admin, reason="Ban")

    def test_self_ban(self):
        """
        Self banning should raise an Error
        """

        with self.assertRaises(Error):
            with transaction.atomic():
                ban_user(receiver=self.admin, creator=self.admin)

    def test_ban_with_common_user_as_creator(self):
        """
        Creating a ban with a common user as creator should raise an Error.
        Bans can only be created by admins
        """

        with self.assertRaises(Error):
            with transaction.atomic():
                ban_user(receiver=self.admin, creator=self.user)

    def test_ban_with_admin_as_receiver(self):
        """
        Creating a ban with an admin as receiver should raise an Error.
        Admins cannot be banned
        """

        with self.assertRaises(Error):
            with transaction.atomic():
                ban_user(receiver=self.admin, creator=self.second_admin)
