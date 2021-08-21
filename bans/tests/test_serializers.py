from utils.tests import ExtendedTestCase

from ..serializers import BannedUserSerializer
from ..services import ban


class BannedUserSerializerTestCase(ExtendedTestCase):
    serializer_class = BannedUserSerializer

    def test_serializer_with_instance(self):
        user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")
        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")
        ban_object = ban(receiver=user, creator=admin, reason="Ban")
        serializer = self.serializer_class(ban_object)
        data = serializer.data

        self.assertEqual(len(data), 4)
        self.assertIn("bannedAt", data)
        self.assertEqual(data["reason"], ban_object.reason)
        self.assertEqual(len(data["receiver"]), 4)
        self.assertEqual(data["receiver"]["login"], ban_object.receiver.login)
        self.assertEqual(len(data["creator"]), 4)
        self.assertEqual(data["creator"]["login"], ban_object.creator.login)
