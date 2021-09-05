from datetime import datetime
from django.db import transaction, Error

from utils.tests import ExtendedTestCase

from ..models import VerificationCode


class VerificationCodeModelTestCase(ExtendedTestCase):
    model = VerificationCode

    def test_verification_code(self):
        user = self.UserModel.objects.create_user(
            login="User",
            email="user@gmail.com",
            password="pass",
            is_active=False
        )
        verification_code = self.model.objects.create(user=user, code="ABCD12")

        self.assertIsInstance(verification_code, self.model)

        self.assertEqual(verification_code.code, "ABCD12")
        self.assertEqual(verification_code.user, user)
        self.assertIsInstance(verification_code.created_at, datetime)

    def test_verification_code_with_active_user(self):
        user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")

        with self.assertRaises(Error):
            with transaction.atomic():
                self.model.objects.create(user=user, code="ABCD12")
