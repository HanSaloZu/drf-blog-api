from utils.tests import ExtendedTestCase

from ..models import VerificationCode
from ..services import codes


class CodesTestCase(ExtendedTestCase):
    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser",
            email="first_user@gmail.com",
            password="pass",
            is_active=False
        )
        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser",
            email="second_user@gmail.com",
            password="pass",
            is_active=False
        )

    def test_generate_verification_code(self):
        """
        generate_verification_code function should return a 6 character string
        """
        verification_code = codes.generate_verification_code()

        self.assertIsInstance(verification_code, str)
        self.assertEqual(len(verification_code), 6)

    def test_create_verification_code(self):
        """
        create_verification_code should create and return
        VerificationCode object
        """
        first_verification_code = codes.create_verification_code(
            self.first_user)
        second_verification_code = codes.create_verification_code(
            self.second_user)

        self.assertIsInstance(first_verification_code, VerificationCode)
        self.assertEqual(VerificationCode.objects.all().count(), 2)
        self.assertEqual(first_verification_code.user, self.first_user)
        self.assertEqual(second_verification_code.user, self.second_user)
        self.assertNotEqual(first_verification_code.code,
                            second_verification_code.code)

    def test_verify_email_by_code(self):
        """
        verify_email_by_code function should delete VerificationCode object
        with a code equal to the one passed in the function parameters
        and activate the user associated with this code
        """
        verification_code = codes.create_verification_code(
            self.first_user).code
        codes.verify_email_by_code(verification_code)

        self.assertEqual(VerificationCode.objects.all().count(), 0)
        self.assertIs(self.UserModel.objects.get(
            id=self.first_user.id).is_active, True)
