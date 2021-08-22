from utils.tests import ExtendedTestCase

from ..serializers import UserSerializer


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
