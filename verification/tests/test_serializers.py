from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..models import VerificationCode
from ..serializers import VerificationCodeSerializer


class VerificationCodeSerializerTestCase(ExtendedTestCase):
    serializer_class = VerificationCodeSerializer

    def test_valid_serializer(self):
        user = self.UserModel.objects.create_user(
            login="User",
            email="user@gmail.com",
            password="pass",
            is_active=False
        )
        VerificationCode.objects.create(user=user, code="AAAAAA")

        data = {
            "code": "AAAAAA"
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["code"], data["code"])

    def test_invalid_serializer(self):
        data = {
            "code": ""
        }
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Verification code cannot be empty", errors)

    def test_serializer_without_data(self):
        """
        The serializer without data should be invalid
        because it has 1 required field
        """
        serializer = self.serializer_class(data={})
        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Verification code field is required", errors)

    def test_serializer_with_non_existent_code(self):
        """
        Serializer with non-existent code should be invalid
        """
        data = {
            "code": "ABCDEF"
        }
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Verification code is invalid or expired", errors)
