from django.urls import reverse

from ..models import FollowersModel
from utils.test import APIViewTestCase


class FollowingAPIViewTestCase(APIViewTestCase):
    model = FollowersModel

    def url(self, kwargs):
        return reverse("follow", kwargs=kwargs)

    def setUp(self):
        first_user_credentials = {
            "email": "first_user_@gmail.com", "password": "pass"}

        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", **first_user_credentials)
        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second_user_@gmail.com", password="pass")
        self.client.login(**first_user_credentials)

    def test_follow(self):
        response = self.client.post(self.url({"user_id": self.second_user.id}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.model.is_following(
            self.first_user, self.second_user))
        self.assertFalse(self.model.is_following(
            self.second_user, self.first_user))

    def test_self_follow(self):
        response = self.client.post(self.url({"user_id": self.first_user.id}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "You can't follow yourself")

    def test_double_following(self):
        self.client.post(self.url({"user_id": self.second_user.id}))
        response = self.client.post(self.url({"user_id": self.second_user.id}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"],
                         "You are already following this user")

    def test_unfollow(self):
        self.client.post(self.url({"user_id": self.second_user.id}))
        response = self.client.delete(
            self.url({"user_id": self.second_user.id}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model.is_following(
            self.first_user, self.second_user))

    def test_unfollow_not_followed_user(self):
        response = self.client.delete(
            self.url(kwargs={"user_id": self.second_user.id}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], "You should first follow the user, then you can unfollow")

    def test_is_following(self):
        response = self.client.get(
            self.url(kwargs={"user_id": self.second_user.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertFalse(response.data["following"])
        self.assertEqual(response.data["following"],
                         self.model.is_following(self.first_user, self.second_user))

        self.client.post(
            self.url(kwargs={"user_id": self.second_user.id}))
        response = self.client.get(
            self.url(kwargs={"user_id": self.second_user.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertTrue(response.data["following"])
        self.assertEqual(response.data["following"],
                         self.model.is_following(self.first_user, self.second_user))

    def test_is_following_with_invalid_user_id(self):
        response = self.client.get(
            self.url(kwargs={"user_id": 999}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_404_NOT_FOUND)

    def test_follow_with_invalid_user_id(self):
        response = self.client.post(self.url(kwargs={"user_id": 999}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_404_NOT_FOUND)

    def test_follow_while_unauthorized(self):
        self.client.logout()

        response = self.client.post(
            self.url(kwargs={"user_id": self.second_user.id}))
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_403_FORBIDDEN)
