from urllib.parse import urlencode
from django.urls import reverse

from utils.test import APIViewTestCase


class UserDetailAPIViewTest(APIViewTestCase):
    url = reverse("user_detail")

    def test_unauthorized_user_request_user_detail(self):
        response = self.client.get(self.url)

        self._common_api_response_tests(
            response, result_code=1, messages_list_len=1)
        message = response.data["messages"][0]
        self.assertEqual(message, "You are not authorized")

    def test_valid_user_detail(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)
        response = self.client.get(self.url)

        self._common_api_response_tests(response)
        response_user_detail = response.data["data"]
        self.assertEqual(response_user_detail["id"], user.id)
        self.assertEqual(response_user_detail["login"], user.login)
        self.assertEqual(response_user_detail["email"], user.email)


class UserAuthenticationAPIViewTest(APIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.credentials)

    def test_authentication_with_valid_data(self):
        response = self.client.put(
            self.url, self.credentials, content_type="application/json")

        self._common_api_response_tests(response)
        self.assertEqual(response.data["data"]["userId"], self.user.id)

    def test_authentication_with_invalid_email(self):
        response = self.client.put(
            self.url, {
                "email": "123",
                "password": self.credentials["password"]
            }, content_type="application/json")

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=1, fields_errors_list_len=1)
        self.assertEqual(response.data["messages"][0], "Enter valid Email")
        self.assertEqual(response.data["fieldsErrors"][0]["field"], "email")
        self.assertEqual(response.data["fieldsErrors"]
                         [0]["error"], "Enter valid Email")

    def test_authentication_with_invalid_password(self):
        response = self.client.put(
            self.url, {
                "email": self.credentials["email"],
                "password": "invalid"
            }, content_type="application/json")

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=1, fields_errors_list_len=0)
        self.assertEqual(response.data["messages"]
                         [0], "Incorrect Email or Password")

    def test_authentication_wihout_credentials(self):
        response = self.client.put(self.url)

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=2, fields_errors_list_len=2)
        self.assertIn("Please enter your Email", response.data["messages"])
        self.assertIn("Enter your password", response.data["messages"])

    def test_logging_out(self):
        self.client.login(**self.credentials)
        response = self.client.delete(self.url)
        self._common_api_response_tests(response)

    def test_unauthorized_logging_out(self):
        response = self.client.delete(self.url)
        self._common_api_response_tests(response)


class UsersListAPIViewsTest(APIViewTestCase):
    def url(self, parameters={}):
        url = reverse("users_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def common_users_list_response_tests(self, response, status_code=200, items_list_len=0, total_count=3, error=""):
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(len(response.data["items"]), items_list_len)
        self.assertEqual(response.data["totalCount"], total_count)
        self.assertEqual(response.data["error"], error)

    def setUp(self):
        self.credentials = {"email": "first@gmail.com", "password": "pass"}
        self.first_user = self.UserModel.objects.create_user(
            login="First User", **self.credentials)
        self.second_user = self.UserModel.objects.create_user(
            login="Second User", email="second@gmail.com", password="pass")
        self.third_user = self.UserModel.objects.create_user(
            login="Third User", email="third@gmail.com", password="pass")

    def test_users_list_without_parameters(self):
        response = self.client.get(self.url())

        self.common_users_list_response_tests(response, items_list_len=3)
        user_data = response.data["items"][0]
        self.assertIn("id", user_data)
        self.assertIn("name", user_data)
        self.assertIn("status", user_data)
        self.assertIn("photo", user_data)
        self.assertIn("followed", user_data)

    def test_users_list_with_term(self):
        response = self.client.get(self.url({"term": "First User"}))

        self.common_users_list_response_tests(
            response, items_list_len=1, total_count=1)
        user_data = response.data["items"][0]
        self.assertEqual(user_data["id"], self.first_user.id)
        self.assertEqual(user_data["name"], self.first_user.login)
        self.assertFalse(user_data["followed"])
        self.assertIsNone(user_data["photo"])
        self.assertEqual(user_data["status"], "")

        response = self.client.get(self.url({"term": "3333"}))
        self.common_users_list_response_tests(
            response, items_list_len=0, total_count=0)

    def test_users_list_with_count_parameter(self):
        response = self.client.get(self.url({"count": 2}))
        self.common_users_list_response_tests(response, items_list_len=2)

    def test_users_list_with_invalid_count_parameter(self):
        response = self.client.get(self.url({"count": -5}))
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_users_list_with_large_count_parameter(self):
        response = self.client.get(self.url({"count": 999}))
        self.common_users_list_response_tests(
            response, error="Max page size is 100 items", total_count=0)

    def test_users_list_with_page_parameter(self):
        response = self.client.get(self.url({"count": 1, "page": 1}))

        self.common_users_list_response_tests(response, items_list_len=1)
        user_data = response.data["items"][0]
        self.assertEqual(user_data["id"], self.third_user.id)

        response = self.client.get(self.url({"count": 1, "page": 2}))

        self.common_users_list_response_tests(response, items_list_len=1)
        user_data = response.data["items"][0]
        self.assertEqual(user_data["id"], self.second_user.id)

    def test_users_list_with_friend_flag(self):
        self.client.login(**self.credentials)
        self.first_user.following.create(
            follower_user=self.first_user, following_user=self.second_user)
        response = self.client.get(self.url({"friend": "true"}))

        self.common_users_list_response_tests(
            response, total_count=1, items_list_len=1)
        self.assertEqual(response.data["items"][0]["id"], self.second_user.id)
        self.assertTrue(response.data["items"][0]["followed"])

    def test_users_list_with_friend_flag_while_unauthorized(self):
        self.second_user.following.create(
            follower_user=self.second_user, following_user=self.first_user)
        response = self.client.get(self.url({"friend": "true"}))

        self.common_users_list_response_tests(response, total_count=0)
