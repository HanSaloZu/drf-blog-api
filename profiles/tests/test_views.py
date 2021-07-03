from django.utils.crypto import get_random_string
from django.urls import reverse

import json

from utils.tests import APIViewTestCase, ProfileDetailAPIViewTestCase


class RetrieveUpdateProfileAPIViewTest(ProfileDetailAPIViewTestCase):
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

        self.compare_profile_instance_and_response_data(
            self.user.profile, response.data)

    # Profile update tests

    def test_profile_update_without_contacts(self):
        payload = {
            "fullname": "New User",
            "aboutMe": get_random_string(length=70),
            "isLookingForAJob": True,
            "professionalSkills": "Backend web developer",
            "status": "New status"
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.about_me, payload["aboutMe"])
        self.assertEqual(user.profile.status, payload["status"])
        self.assertEqual(user.profile.is_looking_for_a_job,
                         payload["isLookingForAJob"])
        self.assertEqual(user.profile.professional_skills,
                         payload["professionalSkills"])
        self.compare_profile_instance_and_response_data(
            user.profile, response.data)

    def test_profile_update_with_contacts(self):
        payload = {
            "fullname": "New Fullname",
            "isLookingForAJob": False,
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

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.is_looking_for_a_job,
                         payload["isLookingForAJob"])
        self.assertEqual(user.profile.status, payload["status"])

        self.assertEqual(contacts.github, payload["contacts"]["github"])
        self.assertEqual(contacts.main_link, payload["contacts"]["mainLink"])
        self.assertEqual(contacts.twitter, payload["contacts"]["twitter"])
        self.assertEqual(contacts.facebook,
                         self.user.profile.contacts.facebook)

        self.compare_profile_instance_and_response_data(
            user.profile, response.data)

    def test_profile_update_without_data(self):
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.compare_profile_instance_and_response_data(
            self.user.profile, response.data)

    def test_profile_update_with_invalid_data(self):
        payload = {
            "fullname": "",
            "aboutMe": get_random_string(length=69),
            "status": get_random_string(length=100),
            "professionalSkills": None,
            "isLookingForAJob": "invalid",
            "contacts": None
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages_list_len=6,
            code="invalid",
            messages=[
                "Fullname field cannot be empty",
                "About me field value is too short",
                "Status field value is too long",
                "Professional skills field cannot be null",
                "Invalid value for is looking for a job field",
                "Contacts field cannot be null"
            ],
            fields_errors_dict_len=6
        )

    def test_profile_update_with_invalid_contacts_urls(self):
        payload = {
            "contacts": {
                "github": "123",
                "twitter": None,
                "facebook": get_random_string(length=205),
                "vk": ""
            }
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages_list_len=3,
            code="invalid",
            fields_errors_dict_len=3,
            messages=[
                "Invalid value for github field",
                "Twitter field cannot be null",
                "Facebook field value is too long"
            ]
        )


class UpdatePhotoAPIViewTest(APIViewTestCase):
    url = reverse("profile_photo_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_photo_update_without_payload(self):
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            messages_list_len=1,
            code="invalid",
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )

    def test_photo_update_with_invalid_payload(self):
        response = self.client.put(
            self.url,
            {"image": "test"},
            content_type="multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW")

        self.client_error_response_test(
            response,
            messages_list_len=1,
            code="invalid",
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )


class ProfilePreferencesAPIViewTest(APIViewTestCase):
    url = reverse("profile_preferences")

    def setUp(self):
        credentials = {"login": "NewUser",
                       "email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(**credentials)
        self.user.profile.preferences.theme = "dark"
        self.user.save()
        self.client.login(**credentials)

    def test_get_preferences(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["theme"],
                         self.user.profile.preferences.theme)

    def test_get_preferences_while_unauthorized(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_403_FORBIDDEN)

    def test_update_preferences_with_valid_data(self):
        put_data = {"theme": "light"}
        response = self.client.put(
            self.url, put_data, content_type="application/json")

        self.common_api_response_tests(response)

        self.assertEqual(self.UserModel.objects.first(
        ).profile.preferences.theme, put_data["theme"])

    def test_update_theme_with_blank_value(self):
        response = self.client.put(
            self.url, {"theme": ""}, content_type="application/json")

        self.common_api_response_tests(response, result_code=1, messages_list_len=1,
                                       fields_errors_list_len=1, messages=["Theme value cannot be empty"])

    def test_update_theme_with_null_value(self):
        put_data = {"theme": None}
        response = self.client.put(
            self.url, put_data, content_type="application/json")

        self.common_api_response_tests(response, result_code=1, messages_list_len=1,
                                       fields_errors_list_len=1, messages=["Theme value cannot be null"])

    def test_update_preferences_without_data(self):
        response = self.client.put(self.url)

        self.common_api_response_tests(response, result_code=1, messages_list_len=1,
                                       fields_errors_list_len=1, messages=["Theme field is required"])

    def test_update_preferences_with_invalid_data(self):
        response = self.client.put(
            self.url, {"theme": "a"*320}, content_type="application/json")

        self.common_api_response_tests(response, result_code=1, messages_list_len=1, fields_errors_list_len=1, messages=[
                                       "Theme field max length is 255 symbols"])
