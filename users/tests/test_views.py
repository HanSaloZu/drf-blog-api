from urllib.parse import urlencode

from django.urls import reverse

from followers.services import follow
from utils.tests import APIViewTestCase, ListAPIViewTestCase


class ListCreateUsersAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("users_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        self.first_user = self.UserModel.objects.create_superuser(
            login="FirstUser", email="first@gmail.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        self.third_user = self.UserModel.objects.create_user(
            login="ThirdUser", email="third@gmail.com", password="pass")

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    # List user

    def test_users_list_without_parameters(self):
        response = self.client.get(self.url())

        self.check_common_details_of_list_view_response(
            response, total_items=3, page_size=3)

        list_item = response.data["items"][0]
        self.assertEqual(len(list_item), 6)
        self.assertIn("id", list_item)
        self.assertIn("login", list_item)
        self.assertIn("status", list_item)
        self.assertIn("avatar", list_item)
        self.assertIn("isFollowed", list_item)
        self.assertIn("isAdmin", list_item)

    def test_users_list_with_q_parameter(self):
        response = self.client.get(self.url({"q": "FirstUser"}))

        self.check_common_details_of_list_view_response(
            response, page_size=1, total_items=1)

        list_item = response.data["items"][0]
        self.assertEqual(list_item["id"], self.first_user.id)
        self.assertEqual(list_item["login"], self.first_user.login)
        self.assertIs(list_item["isFollowed"], False)

        response = self.client.get(self.url({"q": "3333"}))
        self.check_common_details_of_list_view_response(response)

    def test_users_list_with_valid_limit_parameter(self):
        response = self.client.get(self.url({"limit": 2}))

        self.check_common_details_of_list_view_response(
            response, total_items=3, total_pages=2, page_size=2)

    def test_users_list_with_negative_limit_parameter(self):
        """
        When the value of the limit parameter is less than 1, error 400 is returned
        """
        response = self.client.get(self.url({"limit": -5}))

        self.client_error_response_test(
            response,
            messages=["Minimum page size is 1 item"]
        )

    def test_users_list_with_large_limit_parameter(self):
        """
        When the value of the limit parameter is greater than 100, error 400 is returned
        """
        response = self.client.get(self.url({"limit": 999}))

        self.client_error_response_test(
            response,
            messages=["Maximum page size is 100 items"]
        )

    def test_users_list_with_valid_page_parameter(self):
        response = self.client.get(self.url({"limit": 1, "page": 1}))
        self.check_common_details_of_list_view_response(
            response, total_items=3, total_pages=3, page_size=1)

        response = self.client.get(self.url({"limit": 1, "page": 2}))
        self.check_common_details_of_list_view_response(
            response, total_items=3, total_pages=3, page_size=1, page_number=2)

    def test_users_list_with_invalid_page_parameter(self):
        """
        Users list with invalid page parameter should return a 400 error
        """
        response = self.client.get(self.url({"limit": 1, "page": "abc"}))

        self.client_error_response_test(
            response,
            messages=["Invalid page number value"]
        )

    def test_users_list_with_invalid_limit_parameter(self):
        """
        Users list with invalid limit parameter should return a 400 error
        """
        response = self.client.get(self.url({"limit": "invalid"}))

        self.client_error_response_test(
            response,
            messages=["Invalid limit value"]
        )

    # Registration

    def test_registration_request_from_authenticated_user(self):
        """
        A registration request from an authenticated user
        should return a 403 status code
        """
        self.first_user = self.UserModel.objects.create_user(
            login="CommonUser", email="common@user.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        payload = {
            "login": "NewUser",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass"
        }
        response = self.client.post(self.url(), payload)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["messages"][0],
                         "You are already authenticated")

    def test_invalid_registration(self):
        """
        Invalid registration request should return a 400 status code
        """
        self.client.credentials()
        payload = {
            "login": "",
            "password1": "1",
            "password2": "1"
        }
        response = self.client.post(self.url(), payload)

        self.client_error_response_test(
            response,
            messages=[
                "Login can't be empty",
                "Email field is required",
                "Password must be at least 4 characters"
            ],
            fields_errors_dict_len=3
        )

    def test_registration_with_used_email(self):
        """
        Registration with the used email should return a 400 error
        """
        self.client.credentials()
        payload = {
            "login": "Test-",
            "email": self.first_user.email,
            "password1": "pass",
            "password2": "pass"
        }

        response = self.client.post(self.url(), payload)

        self.client_error_response_test(
            response,
            fields_errors_dict_len=1,
            messages=["This email is already in use"]
        )

    def test_registration_with_different_passwords(self):
        """
        Registration with different passwords should return a 400 error
        """
        self.client.credentials()
        payload = {
            "login": "Test_",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "different password"
        }

        response = self.client.post(self.url(), payload)

        self.client_error_response_test(
            response,
            fields_errors_dict_len=1,
            messages=["Passwords do not match"]
        )

    def test_valid_registration(self):
        """
        Valid registration should return a 204 status code
        """
        self.client.credentials()
        payload = {
            "login": "Test",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass"
        }

        response = self.client.post(self.url(), payload)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.all().get(login="Test")
        self.assertIs(user.is_active, False)
        self.assertTrue(user.check_password(payload["password1"]))


class RetrieveUserProfileAPIViewTestCase(APIViewTestCase):
    def url(self, kwargs):
        return reverse("user_profile_detail", kwargs=kwargs)

    def setUp(self):
        self.first_user = self.UserModel.objects.create_user(
            login="FirstUser", email="first@gmail.com", password="pass")

        auth_credentials = self.generate_jwt_auth_credentials(self.first_user)
        self.client.credentials(HTTP_AUTHORIZATION=auth_credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second@gmail.com", password="pass")
        profile = self.second_user.profile
        profile.is_looking_for_a_job = True
        profile.professional_skills = "Test"
        profile.contacts.github = "https://github.com/HanSaloZu"
        self.second_user.save()

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_user_profile_detail(self):
        """
        Profile detail with valid login should return a 200 status code
        and a profile representation in the response body
        """
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.second_user.id)
        self.assertNotIn("theme", response.data)

    def test_self_profile_detail(self):
        """
        Profile detail with login equals authenticated user login
        should return a 200 status code and a profile representation
        """
        response = self.client.get(self.url({"login": self.first_user.login}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.first_user.id)
        self.assertNotIn("theme", response.data)

    def test_user_profile_detail_with_invalid_user_login(self):
        """
        Profile detail with invalid login should return a 400 error
        """
        url = self.url(kwargs={"login": "invalid"})
        response = self.client.get(url)

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"])


class ListUserFollowersAPIViewTestCase(ListAPIViewTestCase):
    def url(self, kwargs={}, parameters={}):
        url = reverse("user_followers_list", kwargs=kwargs)
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

        follow(self.first_user, self.second_user)
        follow(self.second_user, self.third_user)

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_followers_list(self):
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )
        self.assertEqual(response.data["items"]
                         [0]["id"], self.first_user.id)

    def test_self_followers_list(self):
        response = self.client.get(self.url({"login": self.first_user.login}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )

    def test_followers_list_with_invalid_login(self):
        response = self.client.get(self.url({"login": "Invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"]
        )


class ListUserFollowingAPIViewTestCase(ListAPIViewTestCase):
    def url(self, kwargs={}, parameters={}):
        url = reverse("user_following_list", kwargs=kwargs)
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

        follow(self.first_user, self.second_user)
        follow(self.first_user, self.third_user)

        follow(self.third_user, self.second_user)
        follow(self.second_user, self.third_user)

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_following_list(self):
        response = self.client.get(self.url({"login": self.second_user.login}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )
        self.assertEqual(response.data["items"]
                         [0]["id"], self.third_user.id)

    def test_self_following_list(self):
        response = self.client.get(self.url({"login": self.first_user.login}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )

    def test_following_list_with_invalid_login(self):
        response = self.client.get(self.url({"login": "Invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"]
        )
