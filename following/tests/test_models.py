from utils.test import ExtendedTestCase
from django.db import IntegrityError, transaction

from ..models import FollowersModel


class FollowersModelTest(ExtendedTestCase):
    model = FollowersModel

    def setUp(self):
        self.f_user = self._create_user(
            login="FirstUser", email="first@user.com", password="pass")
        self.s_user = self._create_user(
            login="SecondUser", email="second@user.com", password="pass")

    def tearDown(self):
        self.model.objects.all().delete()

    def test_valid_following(self):
        pair = self.model.follow(self.f_user, self.s_user)

        s_user_followers = self.s_user.followers.all()
        self.assertEqual(s_user_followers.first(), pair)

    def test_unfollow(self):
        self.model.follow(self.f_user, self.s_user)
        self.model.follow(self.s_user, self.f_user)

        self.model.unfollow(user=self.f_user, subject=self.s_user)

        f_user_follows = self.f_user.following.all()
        self.assertEqual(f_user_follows.exists(), False)

        s_user_follows = self.s_user.following.all()
        self.assertEqual(s_user_follows.exists(), True)
        self.assertEqual(s_user_follows[0].following_user, self.f_user)

    def test_constraint(self):
        self.model.follow(self.f_user, self.s_user)

        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self.model.follow(self.f_user, self.s_user)
            self.fail('Duplicate following allowed')
        except IntegrityError:
            pass
