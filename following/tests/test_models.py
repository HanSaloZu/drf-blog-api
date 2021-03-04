from utils.test import ExtendedTestCase
from django.db import IntegrityError, transaction

from following.models import FollowersModel


class FollowersModelTest(ExtendedTestCase):
    def setUp(self):
        self.f_user = self._create_user(
            login="FirstUser", email="first@user.com", password="pass", is_superuser=False)
        self.s_user = self._create_user(
            login="SecondUser", email="second@user.com", password="pass", is_superuser=False)

    def _follow(self, follower, follows):
        return FollowersModel.objects.create(
            follower_user=follower, following_user=follows)

    def tearDown(self):
        FollowersModel.objects.all().delete()

    def test_valid_following(self):
        pair = self._follow(self.f_user, self.s_user)
        pair.save()

        s_user_followers = FollowersModel.objects.filter(
            following_user=self.s_user)
        self.assertEqual(s_user_followers.get(follower_user=self.f_user), pair)

    def test_unfollow(self):
        self._follow(self.f_user, self.s_user).save()
        self._follow(self.s_user, self.f_user).save()

        FollowersModel.objects.filter(
            follower_user=self.f_user).delete()

        f_user_follows = FollowersModel.objects.filter(
            follower_user=self.f_user)
        self.assertEqual(f_user_follows.exists(), False)

        s_user_follows = FollowersModel.objects.filter(
            follower_user=self.s_user)
        self.assertEqual(s_user_follows.exists(), True)
        self.assertEqual(s_user_follows[0].following_user, self.f_user)

    def test_constraint(self):
        pair = self._follow(self.f_user, self.s_user)
        pair.save()

        try:
            # Duplicates should be prevented.
            with transaction.atomic():
                self._follow(self.f_user, self.s_user)
            self.fail('Duplicate following allowed.')
        except IntegrityError:
            pass
