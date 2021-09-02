from django.test import TestCase

from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..serializers import LoginSerializer, RegistrationSerializer


class LoginSerializerTestCase(TestCase):
    serializer_class = LoginSerializer

    def test_valid_serializer(self):
        data = {
            "email": "test@test.com",
            "password": "pass"
        }
        serializer = self.serializer_class(data=data)

        self.assertIs(serializer.is_valid(), True)
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_without_data(self):
        """
        The serializer without data should be invalid
        because it has 2 required fields
        """
        serializer = self.serializer_class(data={})

        self.assertIs(serializer.is_valid(), False)

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 2)
        self.assertIn("Enter your email", errors)
        self.assertIn("Enter your password", errors)

    def test_invalid_serializer(self):
        data = {
            "email": "invalid",
            "password": "pass"
        }
        serializer = self.serializer_class(data=data)

        self.assertIs(serializer.is_valid(), False)

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid email", errors)
