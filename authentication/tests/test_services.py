from utils.tests import ExtendedTestCase

from ..services.activation import generate_uidb64, get_user_by_uidb64_or_none
from ..tokens import confirmation_token


class uidb64GenerationTest(ExtendedTestCase):
    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")

    def test_generate_uidb64_and_get_user_using_it(self):
        uidb64 = generate_uidb64(self.user)
        user = get_user_by_uidb64_or_none(uidb64)

        self.assertIsInstance(user, self.UserModel)
        self.assertEqual(user.id, self.user.id)

    def test_get_user_using_invalid_uidb64(self):
        user = get_user_by_uidb64_or_none("invalid")

        self.assertIsNone(user)


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
