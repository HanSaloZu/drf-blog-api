from django.test import TestCase
from django.utils.crypto import get_random_string

from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..serializers import LoginSerializer, RegistrationSerializer


class LoginSerializerTest(TestCase):
    serializer_class = LoginSerializer

    def test_valid_serializer(self):
        data = {
            "email": "test@test.com",
            "password": "pass"
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)

    def test_serializer_without_data(self):
        serializer = self.serializer_class(data={})

        self.assertFalse(serializer.is_valid())

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

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("Invalid email", errors)


class RegistrationSerializerTest(ExtendedTestCase):
    serializer_class = RegistrationSerializer

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="User", email="unique@email.com", password="pass")

    def test_valid_serializer(self):
        data = {
            "login": "NewUser",
            "email": "new@user.com",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "aboutMe": get_random_string(length=80)
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)

    def test_invalid_serializer(self):
        data = {
            "login": "New:;.!?@User",
            "email": None,
            "password1": "s",
            "aboutMe": ""
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 5)
        self.assertIn(
            "Login can only contain letters, numbers, underscores and hyphens", errors)
        self.assertIn("Email is required", errors)
        self.assertIn("Password must be at least 4 characters", errors)
        self.assertIn("You should repeat your password", errors)
        self.assertIn("About me can't be empty", errors)

    def test_serializer_with_non_unique_login(self):
        data = {
            "login": "User",
            "email": "new@user.com",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "aboutMe": get_random_string(length=80)
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("This login is already in use", errors)
