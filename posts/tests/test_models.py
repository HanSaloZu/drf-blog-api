from datetime import datetime

from utils.tests import ExtendedTestCase

from ..models import Post


class PostModelTestCase(ExtendedTestCase):
    model = Post

    def test_post_model(self):
        user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        post = self.model.objects.create(
            author=user, title="Test post", body="Body")

        self.assertIsInstance(post, self.model)

        self.assertEqual(post.author, user)
        self.assertEqual(post.title, "Test post")
        self.assertEqual(post.body, "Body")
        self.assertIsInstance(post.created_at, datetime)
        self.assertIsInstance(post.updated_at, datetime)
