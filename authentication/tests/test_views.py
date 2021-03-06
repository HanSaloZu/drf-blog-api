from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from bans.services import ban_user
from utils.tests import APIViewTestCase


class BaseTestCase(APIViewTestCase):
    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.inactive_user_credentials = {
            "email": "inactive@user.com", "password": "pass"}
        self.banned_user_credentials = {
            "email": "banned@user.com", "password": "pass"}

        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.credentials)
        self.inactive_user = self.UserModel.objects.create_user(
            login="InactiveUser",
            **self.inactive_user_credentials,
            is_active=False
        )
        self.banned_user = self.UserModel.objects.create_user(
            login="BannedUser", **self.banned_user_credentials)

        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@user.com", password="pass")
        ban_user(receiver=self.banned_user, creator=admin)


class CustomObtainTokenPairAPIViewTestCase(BaseTestCase):
    url = reverse("token_create")

    def test_valid_token_obtaining(self):
        """
        Valid token obtaining should return a 200 status code
        and a token pair
        """
        response = self.client.post(self.url, self.credentials)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtaining_by_inactive_user(self):
        """
        Token obtaining by inactive users should return a 403 error
        """
        response = self.client.post(self.url, self.inactive_user_credentials)

        self.client_error_response_test(
            response,
            code="inactiveProfile",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["Your profile is not activated"]
        )

    def test_token_obtaining_by_banned_user(self):
        """
        Token obtaining by banned users should return a 403 error
        """
        response = self.client.post(self.url, self.banned_user_credentials)

        self.client_error_response_test(
            response,
            code="bannedUser",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are banned"]
        )

    def test_token_obtaining_with_invalid_credentials(self):
        """
        Token obtaining with invalid credentials should return a 400 error
        """
        payload = {
            "email": self.credentials["email"],
            "password": "invalid"
        }
        response = self.client.post(self.url, payload)

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            messages=["Incorrect email or password"]
        )

    def test_token_obtaining_wihout_credentials(self):
        """
        Token obtaining without credentials should return a 400 error
        """
        response = self.client.post(self.url)

        self.client_error_response_test(
            response,
            fields_errors_dict_len=2,
            messages=["Enter your email", "Enter your password"]
        )


class CustomTokenRefreshAPIViewTestCase(BaseTestCase):
    url = reverse("token_refresh")

    def test_valid_token_refreshing(self):
        """
        Valid token refreshing should return a 200 status code and a token pair
        """
        payload = {
            "refresh": str(RefreshToken.for_user(self.user))
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_invalid_token_refreshing(self):
        """
        Invalid token refreshing should return a 401 error
        """
        payload = {
            "refresh": "invalid"
        }
        response = self.client.post(self.url, payload)

        self.client_error_response_test(
            response,
            code="notAuthenticated",
            status=self.http_status.HTTP_401_UNAUTHORIZED,
            messages=["You are not authenticated"]
        )

    def test_token_refreshing_without_payload(self):
        """
        Token refreshing without payload should return a 400 error
        """
        response = self.client.post(self.url, {})

        self.client_error_response_test(
            response,
            messages=["Refresh token is required"],
            fields_errors_dict_len=1
        )

    def test_token_refreshing_by_banned_user(self):
        """
        Token refreshing by banned users should return a 403 error
        """
        payload = {
            "refresh": str(RefreshToken.for_user(self.banned_user))
        }
        response = self.client.post(self.url, payload)

        self.client_error_response_test(
            response,
            code="bannedUser",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are banned"]
        )

    def test_token_refreshing_by_inactive_user(self):
        """
        Token refreshing by inactive users should return a 401 error
        """
        payload = {
            "refresh": str(RefreshToken.for_user(self.inactive_user))
        }
        response = self.client.post(self.url, payload)

        self.client_error_response_test(
            response,
            code="notAuthenticated",
            status=self.http_status.HTTP_401_UNAUTHORIZED,
            messages=["You are not authenticated"]
        )
