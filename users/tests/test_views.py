from urllib.parse import urlencode
from django.urls import reverse

from utils.test import APIViewTestCase, ProfileDetailAPIViewTestCase


class UsersListAPIViewsTest(APIViewTestCase):
    def url(self, parameters={}):
        url = reverse("users_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def common_users_list_response_tests(self, response, status_code=200, items_list_len=0, total_count=3):
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(len(response.data["items"]), items_list_len)
        self.assertEqual(response.data["totalCount"], total_count)

    def setUp(self):
        credentials = {"email": "first@gmail.com", "password": "pass"}
        self.first_user = self.UserModel.objects.create_user(
            login="First User", **credentials)
        self.second_user = self.UserModel.objects.create_user(
            login="Second User", email="second@gmail.com", password="pass")
        self.third_user = self.UserModel.objects.create_user(
            login="Third User", email="third@gmail.com", password="pass")
        self.client.login(**credentials)

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
                         self.http_status.HTTP_400_BAD_REQUEST)

    def test_users_list_with_large_count_parameter(self):
        response = self.client.get(self.url({"count": 999}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)

    def test_users_list_with_page_parameter(self):
        response = self.client.get(self.url({"count": 1, "page": 1}))

        self.common_users_list_response_tests(response, items_list_len=1)
        user_data = response.data["items"][0]
        self.assertEqual(user_data["id"], self.third_user.id)

        response = self.client.get(self.url({"count": 1, "page": 2}))

        self.common_users_list_response_tests(response, items_list_len=1)
        user_data = response.data["items"][0]
        self.assertEqual(user_data["id"], self.second_user.id)

    def test_users_list_with_invalid_page_parameter(self):
        response = self.client.get(self.url({"count": 1, "page": "abc"}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)

    def test_users_list_while_unauthorized(self):
        self.client.logout()
        self.second_user.following.create(
            follower_user=self.second_user, following_user=self.first_user)
        response = self.client.get(self.url({"friend": "true"}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_403_FORBIDDEN)


class UserProfileDetailAPIViewTest(ProfileDetailAPIViewTestCase):
    def url(self, kwargs):
        return reverse("user_profile_detail", kwargs=kwargs)

    def setUp(self):
        credentials = {"email": "first@gmail.com", "password": "pass"}
        self.first_user = self.UserModel.objects.create_user(
            login="First User", **credentials)
        self.client.login(**credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="Second User", email="second@gmail.com", password="pass")
        profile = self.second_user.profile
        profile.looking_for_a_job = True
        profile.looking_for_a_job_description = "Test"
        profile.about_me = "Test"
        profile.contacts.github = "https://github.com/HanSaloZu"
        self.second_user.save()

    def test_user_profile_detail(self):
        response = self.client.get(self.url({"login": self.second_user.login}))
        profile = self.second_user.profile

        self.compare_profile_instance_and_response_data(profile, response.data)

    def test_self_profile_detail(self):
        response = self.client.get(self.url({"login": self.first_user.login}))
        profile = self.first_user.profile

        self.compare_profile_instance_and_response_data(profile, response.data)

    def test_user_profile_detail_with_invalid_user_login(self):
        url = self.url(kwargs={"login": "invalid"})
        response = self.client.get(url)

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages_list_len=1,
            messages=["Invalid login, user is not found"])

    def test_user_profile_detail_while_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url({"login": self.second_user}))

        self.client_error_response_test(
            response,
            code="notAuthenticated",
            status=self.http_status.HTTP_401_UNAUTHORIZED,
            messages_list_len=1,
            messages=["You are not authenticated"])
