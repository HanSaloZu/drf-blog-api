from datetime import datetime

from django.db import Error, IntegrityError, transaction

from utils.tests import ExtendedTestCase

from ..models import Attachment, Like, Post


class PostModelTestCase(ExtendedTestCase):
    model = Post

    def test_post_model(self):
        user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        post = self.model.objects.create(author=user, body="Body")

        self.assertIsInstance(post, self.model)

        self.assertEqual(post.author, user)
        self.assertEqual(post.body, "Body")
        self.assertIsInstance(post.created_at, datetime)
        self.assertIsInstance(post.updated_at, datetime)


class LikeModelTestCase(ExtendedTestCase):
    model = Like

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        self.post = Post.objects.create(author=self.user, body="Body")

    def test_valid_like(self):
        self.model.objects.create(user=self.user, post=self.post)
        like_object = self.model.objects.all().first()

        self.assertEqual(self.model.objects.all().count(), 1)
        self.assertEqual(like_object.user, self.user)
        self.assertEqual(like_object.post, self.post)

    def test_double_like(self):
        """
        Double like should raise an IntegrityError
        """
        self.model.objects.create(user=self.user, post=self.post)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.model.objects.create(user=self.user, post=self.post)


class AttachmentModelTestCase(ExtendedTestCase):
    model = Attachment

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        self.post = Post.objects.create(author=self.user, body="Body")

    def test_create_attachment(self):
        self.model.objects.create(
            post=self.post, file_id="1", link="http://localhost:8000/1")
        attachment = self.model.objects.get(post=self.post)

        self.assertIsInstance(attachment, Attachment)

        self.assertEqual(attachment.file_id, "1")
        self.assertEqual(attachment.link, "http://localhost:8000/1")

    def test_create_attachments_over_limit(self):
        """
        The maximum number of attachments for a post is 5.
        When creating attachments over the limit, an error should be raised
        """
        for i in range(5):
            self.model.objects.create(
                post=self.post, file_id=f"{i}", link=f"http://localhost:8000/{i}")

        with self.assertRaises(Error):
            with transaction.atomic():
                self.model.objects.create(
                    post=self.post,
                    file_id="5",
                    link=f"http://localhost:8000/5"
                )
