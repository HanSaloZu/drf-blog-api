from utils.test import ExtendedTestCase


class UserModelTests(ExtendedTestCase):
    def test_user(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass", is_superuser=False)

        self.assertTrue(isinstance(user, self.UserModel))
        self.assertEqual(user.login, "NewUser")
        self.assertEqual(user.email, "new@user.com")

    def test_superuser(self):
        superuser = self._create_user(login="NewSuperuser", email="new@superuser.com",
                                      password="pass", is_superuser=True)

        self.assertTrue(isinstance(superuser, self.UserModel))
        self.assertTrue(superuser.is_superuser)
