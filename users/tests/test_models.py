from utils.tests import ExtendedTestCase


class UserModelTestCase(ExtendedTestCase):
    def test_user(self):
        user_email = "new@user.com"
        user_login = "NewUser"
        user = self.UserModel.objects.create_user(
            login=user_login, email=user_email, password="pass")

        self.assertIsInstance(user, self.UserModel)

        self.assertEqual(user.login, user_login)
        self.assertEqual(user.email, user_email)
        self.assertIs(user.is_superuser, False)
        self.assertIs(user.is_staff, False)
        self.assertIs(user.is_active, True)

    def test_superuser(self):
        superuser_email = "new@superuser.com"
        superuser_login = "NewSuperuser"
        superuser = self.UserModel.objects.create_superuser(
            login=superuser_login, email=superuser_email, password="pass")

        self.assertIsInstance(superuser, self.UserModel)

        self.assertEqual(superuser.login, superuser_login)
        self.assertEqual(superuser.email, superuser_email)
        self.assertIs(superuser.is_superuser, True)
        self.assertIs(superuser.is_staff, True)
        self.assertIs(superuser.is_active, True)
