from django.urls import reverse
from urllib.parse import urlencode

from utils.tests import ListAPIViewTestCase, APIViewTestCase

from ..models import FollowersModel


class FollowingAPIViewTest(APIViewTestCase):
    model = FollowersModel

    def url(self, kwargs):
        return reverse("following", kwargs=kwargs)

    def setUp(self):
        credentials = {
            "email": "first_user_@gmail.com", "password": "pass"}

        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", **credentials)
        self.client.login(**credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second_user_@gmail.com", password="pass")

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_follow(self):
        response = self.client.put(self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.model.is_following(
            self.first_user, self.second_user))
        self.assertFalse(self.model.is_following(
            self.second_user, self.first_user))

    def test_self_follow(self):
        response = self.client.put(self.url({"login": self.first_user.login}))

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            messages=["You can't follow yourself"]
        )

    def test_double_follow(self):
        self.model.follow(self.first_user, self.second_user)

        response = self.client.put(self.url({"login": self.second_user.login}))

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            messages=["You are already following this user"]
        )

    def test_follow_with_invalid_login(self):
        response = self.client.put(self.url({"login": "login"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages_list_len=1,
            messages=["Invalid login, user is not found"]
        )

    def test_unfollow(self):
        self.model.follow(self.first_user, self.second_user)

        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model.is_following(
            self.first_user, self.second_user))

    def test_unfollow_not_followed_user(self):
        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.model.is_following(
            self.first_user, self.second_user))

    def test_is_following(self):
        response = self.client.get(self.url({"login": self.second_user.login}))
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_404_NOT_FOUND)

        self.model.follow(self.first_user, self.second_user)
        response = self.client.get(self.url({"login": self.second_user.login}))
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    def test_is_following_with_invalid_login(self):
        response = self.client.get(self.url({"login": "invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages_list_len=1,
            messages=["Invalid login, user is not found"]
        )
