from django.utils.crypto import get_random_string
from django.urls import reverse

from utils.tests import APIViewTestCase


class RetrieveUpdateProfileAPIViewTestCase(APIViewTestCase):
    url = reverse("profile")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)

        user.profile.is_looking_for_a_job = True
        user.profile.professional_skills = "Test"
        user.profile.about_me = "I am a view test"
        user.profile.contacts.github = "https://github.com/HanSaloZu"
        user.save()

        self.user = user
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.unauthorized_client_error_response_test(response)

    # Profile retrieving tests

    def test_profile_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    # Profile update tests

    def test_profile_update_without_contacts(self):
        """
        Profile update without contacts is valid and should return a 200 status code and a profile representation in the response body
        """
        payload = {
            "fullname": "New User",
            "aboutMe": get_random_string(length=70),
            "isLookingForAJob": True,
            "professionalSkills": "Backend web developer",
            "status": "New status",
            "location": "Berlin",
            "birthday": "2000-01-19"
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.about_me, payload["aboutMe"])
        self.assertEqual(user.profile.status, payload["status"])
        self.assertEqual(str(user.profile.birthday), payload["birthday"])
        self.assertEqual(user.profile.location, payload["location"])

        self.assertEqual(user.profile.is_looking_for_a_job,
                         payload["isLookingForAJob"])
        self.assertEqual(user.profile.professional_skills,
                         payload["professionalSkills"])

    def test_profile_update_with_contacts(self):
        """
        Valid profile update should return a 200 status code and a profile representation in the response body
        """
        payload = {
            "fullname": "New Fullname",
            "status": "",
            "contacts": {
                "github": "https://github.com/HanSaloZu",
                "mainLink": "https://github.com/HanSaloZu",
                "twitter": ""
            }
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")
        user = self.UserModel.objects.all().first()
        contacts = user.profile.contacts

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.status, payload["status"])

        self.assertEqual(contacts.github, payload["contacts"]["github"])
        self.assertEqual(contacts.main_link, payload["contacts"]["mainLink"])
        self.assertEqual(contacts.twitter, payload["contacts"]["twitter"])
        self.assertEqual(contacts.facebook,
                         self.user.profile.contacts.facebook)

    def test_profile_update_without_payload(self):
        """
        Profile update without payload is valid and should return a 200 status code and a profile representation in the response body
        """
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_profile_update_with_invalid_payload(self):
        """
        Profile update with invalid payload should return a 400 status code
        """
        payload = {
            "fullname": "",
            "location": "a"*290,
            "contacts": {
                "github": "123",
            }
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=[
                "Fullname field cannot be empty",
                "Location field value is too long",
                "Invalid value for github field",
            ],
            fields_errors_dict_len=3
        )


class UpdateAvatarAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_avatar_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_avatar_update_without_payload(self):
        """
        Avatar update without payload should return a 400 error
        """
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )

    def test_avatar_update_with_invalid_payload(self):
        """
        Avatar update with invalid payload should return a 400 error
        """
        response = self.client.put(
            self.url,
            {"avatar": "test"},
            content_type="multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW")

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )


class UpdateBannerAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_banner_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_banner_update_without_payload(self):
        """
        Banner update without payload should return a 400 error
        """
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )

    def test_banner_update_with_invalid_payload(self):
        """
        Banner update with invalid payload should return a 400 error
        """
        response = self.client.put(
            self.url,
            {"banner": "test"},
            content_type="multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW")

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )


class RetrieveUpdatePreferencesAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_preferences")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)

        self.user.profile.preferences.theme = "dark"
        self.user.save()

        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.unauthorized_client_error_response_test(response)

    # Preferences retrieving tests

    def test_get_preferences(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["theme"],
                         self.user.profile.preferences.theme)

     # Preferences update tests

    def test_update_preferences(self):
        """
        Valid preferences update should return a 200 status code and a preferences representation in the response body
        """
        payload = {"theme": "light"}
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        user = self.UserModel.objects.first()
        self.assertEqual(user.profile.preferences.theme, payload["theme"])
        self.assertEqual(response.data["theme"], payload["theme"])

    def test_update_preferences_with_invalid_payload(self):
        """
        Preferences update with invalid payload should return a 400 error
        """
        payload = {"theme": None}
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Theme field cannot be null"],
            fields_errors_dict_len=1
        )


class UpdatePasswordAPIViewTestCase(APIViewTestCase):
    url = reverse("update_password")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)

        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_update_password(self):
        """
        Valid password update should return a 204 status code
        """
        payload = {
            "oldPassword": "pass",
            "newPassword1": "newpassword",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.all().first()
        self.assertIs(user.check_password(payload["newPassword1"]), True)

    def test_update_password_with_different_passwords(self):
        """
        Password update with different passwords should return a 400 error
        """
        payload = {
            "oldPassword": "pass",
            "newPassword1": "invalid",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Passwords do not match"],
            fields_errors_dict_len=1
        )

    def test_update_password_with_invalid_current_password(self):
        """
        Password update with invalid current password should return a 400 error
        """
        payload = {
            "oldPassword": "invalid",
            "newPassword1": "newpassword",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Invalid password"],
            fields_errors_dict_len=1
        )
