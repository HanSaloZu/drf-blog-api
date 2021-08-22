from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.tests import APIViewTestCase

from ..services.activation import generate_uidb64
from ..tokens import confirmation_token

from bans.services import ban


class AuthenticationAPIViewTestCase(APIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.inactive_user_credentials = {
            "email": "inactive@user.com", "password": "pass"}
        self.banned_user_credentials = {
            "email": "banned@user.com", "password": "pass"}

        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.credentials)
        self.inactive_user = self.UserModel.objects.create_user(
            login="InactiveUser", **self.inactive_user_credentials, is_active=False
        )
        self.banned_user = self.UserModel.objects.create_user(
            login="BannedUser", **self.banned_user_credentials)

        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@user.com", password="pass")
        ban(receiver=self.banned_user, creator=admin)

    # Authentication test

    def test_valid_authentication(self):
        """
        Valid authentication should return a 200 status code
        and a profile representation in the response body
        """
        response = self.client.put(
            self.url, self.credentials, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_inactive_user_authentication(self):
        """
        Authentication of inactive users should return a 403 error
        """
        response = self.client.put(
            self.url, self.inactive_user_credentials, content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["Your profile is not activated"]
        )

    def test_banned_user_authentication(self):
        """
        Authentication of banned users should return a 403 error
        """
        response = self.client.put(self.url, self.banned_user_credentials,
                                   content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are banned"]
        )

    def test_authentication_with_invalid_password(self):
        """
        Authentication with invalid password should return a 400 error
        """
        payload = {
            "email": self.credentials["email"],
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
        """
        Authentication without credentials should return a 400 error
        """
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            fields_errors_dict_len=2,
            messages=["Enter your email", "Enter your password"]
        )

    # Logout test

    def test_valid_logout(self):
        """
        Valid logout should return a 204 status code
        """
        self.client.login(**self.credentials)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_client_logout(self):
        """
        Logging out by an unauthenticated client should return a 204 status code
        """
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    # Registration test

    def test_registration_request_by_authenticated_client(self):
        """
        A registration request from an authenticated client should return a 403 error
        """
        self.client.login(**self.credentials)

        payload = {
            "login": "NewUser",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80),
            "location": "London",
            "birthday": "1997-08-21"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are already authenticated"]
        )

    def test_registration_with_used_email(self):
        """
        Registration with the used email should return a 400 error
        """
        payload = {
            "login": "Test-",
            "email": self.credentials["email"],
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80),
            "location": "London",
            "birthday": "1997-08-21"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            fields_errors_dict_len=1,
            messages=["This email is already in use"]
        )

    def test_registration_with_different_passwords(self):
        """
        Registration with different passwords should return a 400 error
        """
        payload = {
            "login": "Test_",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "different password",
            "aboutMe": get_random_string(length=80),
            "location": "London",
            "birthday": "1997-08-21"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            fields_errors_dict_len=1,
            messages=["Passwords do not match"]
        )

    def test_valid_registration(self):
        """
        Valid registration should return a 204 status code
        """
        payload = {
            "login": "Test",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80),
            "location": "London",
            "birthday": "1997-08-21"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.all().get(login="Test")
        self.assertIs(user.is_active, False)
        self.assertEqual(user.profile.about_me, payload["aboutMe"])
        self.assertEqual(user.profile.location, payload["location"])
        self.assertEqual(str(user.profile.birthday), payload["birthday"])
        self.assertIs(user.check_password(payload["password1"]), True)


class ProfileActivationAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_activation")

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass", is_active=False)

    def test_profile_activation_request_by_authenticated_client(self):
        """
        A profile activation request from an authenticated client should return a 403 error
        """
        credentials = {"email": "active@user.com", "password": "pass"}
        self.UserModel.objects.create_user(login="ActiveUser", **credentials)
        self.client.login(**credentials)

        payload = {
            "token": confirmation_token.make_token(self.user),
            "uidb64": generate_uidb64(self.user)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You are already authenticated"]
        )

    def test_valid_profile_activation(self):
        """
        Valid profile activation should return a 204 status code
        """
        payload = {
            "token": confirmation_token.make_token(self.user),
            "uidb64": generate_uidb64(self.user)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.get(id=self.user.id)
        self.assertIs(self.user.is_active, False)
        self.assertIs(user.is_active, True)

    def test_profile_activation_with_invalid_payload(self):
        """
        Profile activation with invalid credentials should return a 400 error
        """
        payload = {
            "token": "invalid",
            "uidb64": "invalid"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Invalid credentials"]
        )
