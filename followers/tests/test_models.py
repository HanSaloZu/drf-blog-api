from django.db import IntegrityError, transaction, Error

from utils.tests import ExtendedTestCase
from ..models import Follower


class FollowerModelTestCase(ExtendedTestCase):
    model = Follower

    def setUp(self):
        self.f_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@user.com", password="pass")
        self.s_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@user.com", password="pass")

    def tearDown(self):
        self.model.objects.all().delete()

    def test_valid_following(self):
        pair = self.model.follow(self.f_user, self.s_user)

        s_user_followers = self.s_user.followers.all()
        self.assertEqual(s_user_followers.first(), pair)

    def test_valid_unfollowing(self):
        self.model.follow(self.f_user, self.s_user)
        self.model.follow(self.s_user, self.f_user)

        self.model.unfollow(user=self.f_user, subject=self.s_user)

        f_user_follows = self.f_user.following.all()
        self.assertIs(f_user_follows.exists(), False)

        s_user_follows = self.s_user.following.all()
        self.assertIs(s_user_follows.exists(), True)
        self.assertEqual(s_user_follows[0].following_user, self.f_user)

    def test_double_following(self):
        """
        Double following should raise an IntegrityError
        """
        self.model.follow(self.f_user, self.s_user)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.model.follow(self.f_user, self.s_user)

    def test_invalid_following(self):
        """
        Following with follower_user == following_user should raise an error
        """
        with self.assertRaises(Error):
            with transaction.atomic():
                self.model.follow(self.f_user, self.f_user)
