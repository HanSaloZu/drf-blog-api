from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..serializers import CreateUserSerializer, UserSerializer


class UserSerializerTestCase(ExtendedTestCase):
    serializer_class = UserSerializer

    def test_serializer_with_common_user_instance(self):
        user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")
        serializer = self.serializer_class(instance=user)

        self.assertEqual(len(serializer.data), 4)
        self.assertEqual(serializer.data["id"], user.id)
        self.assertEqual(serializer.data["login"], user.login)
        self.assertEqual(serializer.data["avatar"], "")
        self.assertIs(serializer.data["isAdmin"], False)

    def test_serializer_with_admin_user_instance(self):
        user = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")
        serializer = self.serializer_class(instance=user)

        self.assertEqual(len(serializer.data), 4)
        self.assertIs(serializer.data["isAdmin"], True)


class CreateUserSerializerTestCase(ExtendedTestCase):
    serializer_class = CreateUserSerializer

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="User", email="unique@email.com", password="pass")

    def test_valid_serializer(self):
        data = {
            "login": "NewUser",
            "email": "new@user.com",
            "password1": "strongpassword",
            "password2": "strongpassword"
        }
        serializer = self.serializer_class(data=data)

        self.assertIs(serializer.is_valid(), True)
        validated_data = dict(serializer.validated_data)
        self.assertEqual(data, validated_data)

    def test_invalid_serializer(self):
        data = {
            "login": "New:;.!?@User",
            "email": None,
            "password1": "s"
        }
        serializer = self.serializer_class(data=data)

        self.assertIs(serializer.is_valid(), False)

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 4)
        self.assertIn(
            ("Login can only contain English letters, numbers, " +
                "underscores and hyphens"),
            errors
        )
        self.assertIn("Email is required", errors)
        self.assertIn("Password must be at least 4 characters", errors)
        self.assertIn("You should repeat your password", errors)

    def test_serializer_with_non_unique_login(self):
        """
        Using a non-unique login makes the serializer invalid
        """
        data = {
            "login": "User",
            "email": "new@user.com",
            "password1": "strongpassword",
            "password2": "strongpassword"
        }
        serializer = self.serializer_class(data=data)

        self.assertIs(serializer.is_valid(), False)

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("This login is already in use", errors)
