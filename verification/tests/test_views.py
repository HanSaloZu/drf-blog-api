from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from utils.tests import APIViewTestCase

from ..services.codes import (create_verification_code,
                              generate_verification_code)


class EmailVerificationAPIViewTestCase(APIViewTestCase):
    url = reverse("verification")

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="User",
            email="user@gmail.com",
            password="pass",
            is_active=False
        )
        self.verification_code = create_verification_code(self.user).code

    def test_request_by_authenticated_user(self):
        """
        Only unauthenticated users can verify email.
        Email verification by an authenticated user should return a 403 error
        """
        new_user = self.UserModel.objects.create_user(
            login="NewUser", email="new_user@gmail.com", password="pass")
        token = RefreshToken.for_user(new_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION="JWT {0}".format(token))

        payload = {
            "code": self.verification_code
        }
        response = self.client.post(self.url, payload)

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are already authenticated"]
        )

    def test_valid_email_verification(self):
        """
        Valid email verification should return a 204 status code
        """
        payload = {
            "code": self.verification_code
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)

    def test_email_verification_without_payload(self):
        """
        Email verification without payload should return a 400 error
        """
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)

        self.client_error_response_test(
            response,
            messages=["Verification code field is required"],
            fields_errors_dict_len=1
        )

    def test_email_verification_with_invalid_code(self):
        """
        Email verification with invalid code should return a 400 error
        """
        payload = {
            "code": generate_verification_code()
        }
        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_400_BAD_REQUEST)

        self.client_error_response_test(
            response,
            messages=["Verification code is invalid or expired"],
            fields_errors_dict_len=1
        )
