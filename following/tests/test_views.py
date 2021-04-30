from django.urls import reverse
from rest_framework import status
import json

from ..models import FollowersModel
from utils.test import APIViewTestCase


class FollowingAPIViewTestCase(APIViewTestCase):
    model = FollowersModel

    def url(self, kwargs):
        return reverse("follow", kwargs=kwargs)

    def setUp(self):
        f_user_credentials = {
            "email": "first_user_@gmail.com", "password": "pass"}

        self.f_user = self._create_user(
            login="FirstUser", **f_user_credentials)
        self.s_user = self._create_user(
            login="SecondUser", email="second_user_@gmail.com", password="pass")
        self.client.login(**f_user_credentials)

    def test_follow(self):
        response = self.client.post(self.url({"user_id": self.s_user.id}))

        self._common_api_response_tests(response)
        self.assertTrue(self.model.is_following(self.f_user, self.s_user))
        self.assertFalse(self.model.is_following(self.s_user, self.f_user))

    def test_self_follow(self):
        response = self.client.post(self.url({"user_id": self.f_user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._common_api_response_tests(
            response, result_code=1, messages_list_len=1)
        self.assertEqual(response.data["messages"]
                         [0], "You can't follow yourself")

    def test_double_following(self):
        self.client.post(self.url({"user_id": self.s_user.id}))

        response = self.client.post(self.url({"user_id": self.s_user.id}))
        self._common_api_response_tests(
            response, result_code=1, messages_list_len=1)
        self.assertEqual(response.data["messages"]
                         [0], "You are already following this user")

    def test_unfollow(self):
        self.client.post(self.url({"user_id": self.s_user.id}))

        response = self.client.delete(self.url({"user_id": self.s_user.id}))
        self._common_api_response_tests(response)
        self.assertFalse(self.model.is_following(self.f_user, self.s_user))

    def test_unfollow_not_followed_user(self):
        response = self.client.delete(
            self.url(kwargs={"user_id": self.s_user.id}))

        self._common_api_response_tests(
            response, result_code=1, messages_list_len=1)
        self.assertEqual(response.data["messages"]
                         [0], "First you should follow user. Then you can unfollow")

    def test_is_following(self):
        response = self.client.get(
            self.url(kwargs={"user_id": self.s_user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json.loads(response.content))
        self.assertEqual(json.loads(response.content),
                         self.model.is_following(self.f_user, self.s_user))

        self.client.post(
            self.url(kwargs={"user_id": self.s_user.id}))
        response = self.client.get(
            self.url(kwargs={"user_id": self.s_user.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content))
        self.assertEqual(json.loads(response.content),
                         self.model.is_following(self.f_user, self.s_user))

    def test_is_following_with_invalid_user_id(self):
        response = self.client.get(
            self.url(kwargs={"user_id": 999}))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Bad request")

    def test_follow_with_invalid_user_id(self):
        response = self.client.post(self.url(kwargs={"user_id": 999}))

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_follow_while_unauthorized(self):
        self.client.logout()

        response = self.client.post(
            self.url(kwargs={"user_id": self.s_user.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
