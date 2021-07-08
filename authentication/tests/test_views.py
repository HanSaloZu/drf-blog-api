from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.tests import ProfileDetailAPIViewTestCase, APIViewTestCase

from ..services.activation import generate_uidb64
from ..tokens import confirmation_token


class AuthenticationAPIViewTest(ProfileDetailAPIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.inactive_user_credentials = {
            "email": "inactive@user.com", "password": "pass"}

        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.credentials)
        self.inactive_user = self.UserModel.objects.create_user(
            login="InactiveUser", **self.inactive_user_credentials, is_active=False
        )

    # Authentication test

    def test_authentication(self):
        response = self.client.put(
            self.url, self.credentials, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.compare_profile_instance_and_response_data(
            self.user.profile, response.data)

    def test_inactive_profile_authentication(self):
        response = self.client.put(
            self.url, self.inactive_user_credentials, content_type="application/json")

        self.client_error_response_test(
            response,
            code="inactiveProfile",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages_list_len=1,
            messages=["Your profile is not activated"]
        )

    def test_authentication_with_invalid_email(self):
        payload = {
            "email": "invalid",
            "password": self.credentials["password"]
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
        self.client.login(**self.credentials)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_client_logout(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

    # Registration test

    def test_registration_request_by_authenticated_client(self):
        self.client.login(**self.credentials)

        payload = {
            "login": "NewUser",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages_list_len=1,
            messages=["You are already autenticated"]
        )

    def test_registration_with_used_login(self):
        payload = {
            "login": "NewUser",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            fields_errors_dict_len=1,
            messages=["This login is already in use"]
        )

    def test_registration_with_invalid_login(self):
        payload = {
            "login": "New:;.!?@User",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            fields_errors_dict_len=1,
            messages=[
                "Login can only contain letters, numbers, underscores and hyphens"
            ]
        )

    def test_registration_with_used_email(self):
        payload = {
            "login": "Test-",
            "email": self.credentials["email"],
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            fields_errors_dict_len=1,
            messages=["This email is already in use"]
        )

    def test_registration_with_different_passwords(self):
        payload = {
            "login": "Test_",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "different password",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=1,
            fields_errors_dict_len=1,
            messages=["Passwords do not match"]
        )

    def test_registration_with_invalid_payload(self):
        payload = {
            "login": get_random_string(length=180),
            "email": None,
            "password1": "s",
            "aboutMe": ""
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="invalid",
            messages_list_len=5,
            fields_errors_dict_len=5,
            messages=[
                "Login must be up to 150 characters long",
                "Email is required",
                "Password must be at least 4 characters",
                "You should repeat your password",
                "About me can't be empty"
            ]
        )

    def test_registration(self):
        payload = {
            "login": "Test",
            "email": "test@test.com",
            "password1": "pass",
            "password2": "pass",
            "aboutMe": get_random_string(length=80)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.all().get(login="Test")
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.about_me, payload["aboutMe"])
        self.assertTrue(user.check_password(payload["password1"]))


class ProfileActivationAPIViewTest(APIViewTestCase):
    url = reverse("profile_activation")

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass", is_active=False)

    def test_profile_activation(self):
        payload = {
            "token": confirmation_token.make_token(self.user),
            "uidb64": generate_uidb64(self.user)
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.get(id=self.user.id)
        self.assertFalse(self.user.is_active)
        self.assertTrue(user.is_active)

    def test_profile_activation_with_invalid_payload(self):
        payload = {
            "token": "invalid",
            "uidb64": "invalid"
        }
        response = self.client.post(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages_list_len=1,
            messages=["Invalid credentials"]
        )
