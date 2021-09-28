from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..serializers import BannedUserSerializer, BanSerializer
from ..services import ban_user


class BannedUserSerializerTestCase(ExtendedTestCase):
    serializer_class = BannedUserSerializer

    def test_serializer_with_instance(self):
        user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")
        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")
        ban_object = ban_user(receiver=user, creator=admin, reason="Ban")
        serializer = self.serializer_class(ban_object)
        data = serializer.data

        self.assertEqual(len(data), 4)
        self.assertIn("bannedAt", data)
        self.assertEqual(data["reason"], ban_object.reason)
        self.assertEqual(len(data["receiver"]), 4)
        self.assertEqual(data["receiver"]["login"], ban_object.receiver.login)
        self.assertEqual(len(data["creator"]), 4)
        self.assertEqual(data["creator"]["login"], ban_object.creator.login)


class BanSerializerTestCase(ExtendedTestCase):
    serializer_class = BanSerializer

    def test_valid_serializer(self):
        data = {
            "reason": "Ban"
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, data)

    def test_invalid_serializer(self):
        data = {
            "reason": None
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())
        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("Reason cannot be null", errors)

    def test_serializer_without_data(self):
        """
        The serializer without data should be valid
        because it has no required fields
        """
        serializer = self.serializer_class(data={})

        self.assertTrue(serializer.is_valid())
