from django.urls import reverse
from urllib.parse import urlencode

from utils.tests import ListAPIViewTestCase, APIViewTestCase

from ..services import follow, is_following, unfollow


class FollowersListAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("followers_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@gmail.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        self.third_user = self.UserModel.objects.create_user(
            login="ThirdUser", email="third@gmail.com", password="pass")

        follow(self.second_user, self.first_user)
        follow(self.third_user, self.first_user)

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
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

    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@gmail.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        follow(self.first_user, self.second_user)

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
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
    def url(self, kwargs):
        return reverse("following", kwargs=kwargs)

    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first_user_@gmail.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second_user_@gmail.com", password="pass")

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_follow(self):
        """
        A valid follow request should return isFollowed: True
        """
        response = self.client.put(self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_200_OK)
        self.assertIs(is_following(self.first_user, self.second_user), True)
        self.assertIs(response.data["isFollowed"], True)

    def test_self_follow(self):
        """
        Self follow should return a 400 error
        """
        response = self.client.put(self.url({"login": self.first_user.login}))

        self.client_error_response_test(
            response,
            messages=["You cannot follow yourself"]
        )
        self.assertIs(is_following(self.first_user, self.first_user), False)

    def test_double_follow(self):
        """
        Duplicate follow should return isFollowed: True
        """
        follow(self.first_user, self.second_user)

        response = self.client.put(self.url({"login": self.second_user.login}))
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_200_OK)
        self.assertIs(is_following(self.first_user, self.second_user), True)
        self.assertIs(response.data["isFollowed"], True)

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
        A valid unfollow request should return isFollowed: False
        """
        follow(self.first_user, self.second_user)

        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_200_OK)
        self.assertIs(is_following(self.first_user, self.second_user), False)
        self.assertIs(response.data["isFollowed"], False)

    def test_unfollow_not_followed_user(self):
        """
        Unfollowing from an unfollowed user should return a 404 error
        """
        response = self.client.delete(
            self.url({"login": self.second_user.login}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["You are not yet followed this user"]
        )
        self.assertIs(is_following(self.first_user, self.second_user), False)

    def test_is_following(self):
        """
        If the user is being followed, isFollowed should be True,
        otherwise False
        """
        response = self.client.get(self.url({"login": self.second_user.login}))
        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isFollowed"], False)

        follow(self.first_user, self.second_user)
        response = self.client.get(self.url({"login": self.second_user.login}))
        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isFollowed"], True)

    def test_is_following_with_invalid_login(self):
        response = self.client.get(self.url({"login": "invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"]
        )
