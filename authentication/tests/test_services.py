from utils.tests import ExtendedTestCase

from ..tokens import confirmation_token


class ProfileActivationTokenGenerationTest(ExtendedTestCase):
    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@user.com", password="pass")

    def test_generate_token_and_check_it(self):
        token = confirmation_token.make_token(self.first_user)
        self.assertTrue(confirmation_token.check_token(self.first_user, token))

    def test_check_token_with_other_user(self):
        token = confirmation_token.make_token(self.first_user)
        self.assertFalse(confirmation_token.check_token(
            self.second_user, token))
