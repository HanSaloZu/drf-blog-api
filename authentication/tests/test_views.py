from django.urls import reverse

from utils.tests import ProfileDetailAPIViewTestCase


class AuthenticationAPIViewTest(ProfileDetailAPIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.login_credentials = {"email": "new@user.com", "password": "pass"}

        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.login_credentials)

    # Authentication test

    def test_authentication(self):
        response = self.client.put(
            self.url, self.login_credentials, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.compare_profile_instance_and_response_data(
            self.user.profile, response.data)

    def test_authentication_with_invalid_email(self):
        payload = {
            "email": "invalid",
            "password": self.login_credentials["password"]
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            fields_errors_dict_len=1,
            messages=["Invalid email"]
        )

    def test_authentication_with_invalid_password(self):
        payload = {
            "email": self.login_credentials["email"],
            "password": "invalid"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            messages=["Incorrect email or password"]
        )

    def test_authentication_wihout_credentials(self):
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=2,
            fields_errors_dict_len=2,
            messages=["Enter your email", "Enter your password"]
        )

    # Logout test

    def test_logout(self):
        self.client.login(**self.login_credentials)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_client_logout(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
