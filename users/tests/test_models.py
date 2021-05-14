from utils.test import ExtendedTestCase


class UserModelTest(ExtendedTestCase):
    def test_user(self):
        user_email = "new@user.com"
        user_login = "NewUser"
        user = self.UserModel.objects.create_user(
            login=user_login, email=user_email, password="pass")

        self.assertIsInstance(user, self.UserModel)

        self.assertEqual(user.login, user_login)
        self.assertEqual(user.email, user_email)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_superuser(self):
        superuser_email = "new@superuser.com"
        superuser_login = "NewSuperuser"
        superuser = self.UserModel.objects.create_superuser(
            login=superuser_login, email=superuser_email, password="pass")

        self.assertIsInstance(superuser, self.UserModel)

        self.assertEqual(superuser.login, superuser_login)
        self.assertEqual(superuser.email, superuser_email)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)
