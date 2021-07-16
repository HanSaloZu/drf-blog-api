from django.urls import reverse
from urllib.parse import urlencode

from utils.tests import ListAPIViewTestCase, APIViewTestCase

from ..models import FollowersModel


class FollowersListAPIViewTestCase(ListAPIViewTestCase):
    model = FollowersModel

    def url(self, parameters={}):
        url = reverse("followers_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        credentials = {"email": "first@gmail.com", "password": "pass"}
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", **credentials)
        self.client.login(**credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        self.third_user = self.UserModel.objects.create_user(
            login="ThirdUser", email="third@gmail.com", password="pass")

        self.model.follow(self.second_user, self.first_user)
        self.model.follow(self.third_user, self.first_user)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    def test_followers_list(self):
        response = self.client.get(self.url())

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )

    def test_followers_list_with_q_parameter(self):
        response = self.client.get(self.url({"q": "SecondUser"}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )
        self.assertEqual(response.data["items"]
                         [0]["id"], self.second_user.id)


class FollowingListAPIViewTestCase(ListAPIViewTestCase):
    url = reverse("following_list")
    model = FollowersModel

    def setUp(self):
        credentials = {"email": "first@gmail.com", "password": "pass"}
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", **credentials)
        self.client.login(**credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        self.model.follow(self.first_user, self.second_user)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_following_list(self):
        response = self.client.get(self.url)

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )
        self.assertEqual(response.data["items"]
                         [0]["id"], self.second_user.id)


class FollowingAPIViewTestCase(APIViewTestCase):
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
        """
        A valid follow request should return a 204 status code
        """
        response = self.client.put(self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertIs(self.model.is_following(
            self.first_user, self.second_user), True)
        self.assertIs(self.model.is_following(
            self.second_user, self.first_user), False)

    def test_self_follow(self):
        """
        Self follow should return a 400 error
        """
        response = self.client.put(self.url({"login": self.first_user.login}))

        self.client_error_response_test(
            response,
            messages=["You can't follow yourself"]
        )

    def test_double_follow(self):
        """
        Duplicate follow should return a 400 error
        """
        self.model.follow(self.first_user, self.second_user)

        response = self.client.put(self.url({"login": self.second_user.login}))

        self.client_error_response_test(
            response,
            messages=["You are already following this user"]
        )

    def test_follow_with_invalid_login(self):
        """
        A follow request with an invalid login should return a 404 error
        """
        response = self.client.put(self.url({"login": "login"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"]
        )

    def test_unfollow(self):
        """
        A valid unfollow request should return a 204 status code
        """
        self.model.follow(self.first_user, self.second_user)

        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertIs(self.model.is_following(
            self.first_user, self.second_user), False)

    def test_unfollow_not_followed_user(self):
        """
        Unfollowing from an unfollowed user does not return an error
        """
        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertIs(self.model.is_following(
            self.first_user, self.second_user), False)

    def test_is_following(self):
        """
        If the user is being followed, the response status code should be 204, otherwise 404
        """
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
            messages=["Invalid login, user is not found"]
        )
