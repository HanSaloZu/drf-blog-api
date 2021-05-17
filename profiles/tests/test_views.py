from django.urls import reverse
import json

from utils.test import APIViewTestCase


class ProfileStatusDetailAPIViewTest(APIViewTestCase):
    def url(self, kwargs):
        return reverse("profile_status_detail", kwargs=kwargs)

    def test_status_detail_with_invalid_user_id(self):
        url = self.url({"user_id": 9})
        response = self.client.get(url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "An error has occurred.")

    def test_valid_status_detail(self):
        user = self.UserModel.objects.create_user(login="NewUser", email="new@user.com",
                                                  password="pass")
        user.profile.status = "test"
        user.save()

        response = self.client.get(self.url({"user_id": 1}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         user.profile.status)


class ProfileStatusUpdateAPIViewTest(APIViewTestCase):
    url = reverse("profile_status_update")

    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.UserModel.objects.create_user(login="NewUser", **self.credentials)
        self.client.login(**self.credentials)

    def test_valid_status_update(self):
        response = self.client.put(
            self.url, {"status": "Test"}, content_type="application/json")

        self.common_api_response_tests(response)
        user = self.UserModel.objects.get(id=1)
        self.assertEqual(user.profile.status, "Test")

    def test_status_update_with_blank_value(self):
        response = self.client.put(
            self.url, {"status": ""}, content_type="application/json")

        self.common_api_response_tests(response)
        user = self.UserModel.objects.get(id=1)
        self.assertEqual(user.profile.status, "")

    def test_status_update_with_none_value(self):
        response = self.client.put(
            self.url, {"status": None}, content_type="application/json")
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_status_update_with_long_value(self):
        response = self.client.put(
            self.url, {"status": "a"*320}, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIn("Max Status length is 300 symbols",
                      response.data["messages"])

    def test_status_update_without_value(self):
        response = self.client.put(self.url)
        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "An error has occurred.")

    def test_status_update_by_unauthorized_user(self):
        self.client.logout()
        response = self.client.put(
            self.url, {"status": "New status"}, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"], "Authorization has been denied for this request.")


class ProfileDetailAPIViewTest(APIViewTestCase):
    def url(self, kwargs):
        return reverse("profile_detail", kwargs=kwargs)

    def setUp(self):
        user = self.UserModel.objects.create_user(login="NewUser", email="new@user.com",
                                                  password="pass")
        profile = user.profile

        profile.looking_for_a_job = True
        profile.looking_for_a_job_description = "Test"
        profile.about_me = "I am a view test"
        profile.contacts.github = "https://github.com/HanSaloZu"
        user.save()
        self.profile = profile

    def test_valid_profile_detail(self):
        url = self.url({"user_id": 1})
        response = self.client.get(url)
        data = response.data
        profile = self.profile

        self.assertEqual(data["userId"], profile.user.id)
        self.assertTrue(data["lookingForAJob"])
        self.assertEqual(data["lookingForAJobDescription"],
                         profile.looking_for_a_job_description)
        self.assertEqual(data["fullName"], profile.fullname)
        self.assertEqual(data["fullName"], profile.user.login)
        self.assertEqual(data["aboutMe"], profile.about_me)
        self.assertEqual(len(data["contacts"]), 8)
        self.assertEqual(data["photo"], profile.photo.link)
        self.assertEqual(data["contacts"]["github"], profile.contacts.github)
        self.assertIsNone(data["contacts"]["facebook"])
        self.assertIsNone(data["contacts"]["instagram"])
        self.assertIsNone(data["contacts"]["mainLink"])
        self.assertIsNone(data["contacts"]["twitter"])
        self.assertIsNone(data["contacts"]["vk"])
        self.assertIsNone(data["contacts"]["website"])
        self.assertIsNone(data["contacts"]["youtube"])

    def test_profile_detail_with_invalid_user_id(self):
        url = reverse("profile_detail", kwargs={"user_id": 9})
        response = self.client.get(url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfilePhotoUpdateAPIViewTest(APIViewTestCase):
    url = reverse("profile_photo_update")

    def setUp(self):
        self.credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.credentials)

    def test_photo_update_by_unauthorized_user(self):
        response = self.client.put(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"], "Authorization has been denied for this request.")

    def test_photo_update_without_file(self):
        self.client.login(**self.credentials)
        response = self.client.put(self.url)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileUpdateAPIViewTest(APIViewTestCase):
    url = reverse("profile_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_profile_update_by_unauthorized_user(self):
        self.client.logout()
        response = self.client.put(
            self.url, {"fullName": "New User", "aboutMe": "About me!"}, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["message"], "Authorization has been denied for this request.")

    def test_profile_update_with_only_required_fields(self):
        request_data = {"fullName": "New User", "aboutMe": "About me!"}
        response = self.client.put(
            self.url, request_data, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.common_api_response_tests(response)
        self.assertEqual(user.profile.fullname, request_data["fullName"])
        self.assertEqual(user.profile.about_me, request_data["aboutMe"])
        self.assertFalse(user.profile.looking_for_a_job)
        self.assertIsNone(user.profile.looking_for_a_job_description)

    def test_profile_update_with_contacts(self):
        request_data = {"fullName": "New User", "aboutMe": "About me!", "contacts": {
            "github": "https://github.com/HanSaloZu",
            "mainLink": "https://github.com/HanSaloZu"
        }}
        response = self.client.put(
            self.url, request_data, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.common_api_response_tests(response)
        self.assertEqual(user.profile.contacts.github,
                         request_data["contacts"]["github"])
        self.assertEqual(user.profile.contacts.main_link,
                         request_data["contacts"]["mainLink"])
        self.assertIsNone(user.profile.contacts.facebook)
        self.assertIsNone(user.profile.contacts.instagram)
        self.assertIsNone(user.profile.contacts.twitter)
        self.assertIsNone(user.profile.contacts.vk)
        self.assertIsNone(user.profile.contacts.website)
        self.assertIsNone(user.profile.contacts.youtube)

    def test_profile_update_without_contacts(self):
        request_data = {"fullName": "New User", "aboutMe": "About me!",
                        "lookingForAJob": True, "lookingForAJobDescription": "I need a job!"}
        response = self.client.put(
            self.url, request_data, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.common_api_response_tests(response)
        self.assertEqual(user.profile.looking_for_a_job,
                         request_data["lookingForAJob"])
        self.assertEqual(user.profile.looking_for_a_job_description,
                         request_data["lookingForAJobDescription"])

    def test_profile_update_without_data(self):
        response = self.client.put(self.url)

        self.common_api_response_tests(
            response, messages_list_len=2, result_code=1, messages=["The FullName field is required. (FullName)", "The AboutMe field is required. (AboutMe)"])

    def test_profile_update_with_invalid_data(self):
        response = self.client.put(
            self.url, {"fullName": None, "aboutMe": None}, content_type="application/json")

        self.common_api_response_tests(
            response, messages_list_len=2, result_code=1, messages=["The FullName field is required. (FullName)", "The AboutMe field is required. (AboutMe)"])

    def test_profile_update_with_invalid_contacts(self):
        response = self.client.put(
            self.url, {"fullName": "New User", "aboutMe": "About me!", "contacts": {
                "github": "123"
            }}, content_type="application/json")

        self.common_api_response_tests(response, messages_list_len=1, result_code=1, messages=[
            "Invalid url format (Contacts->Github)"])

    def test_profile_update_with_contacts_equals_none(self):
        response = self.client.put(
            self.url, {"fullName": "New User", "aboutMe": "About me!", "contacts": None}, content_type="application/json")

        self.common_api_response_tests(response)


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
                         self.http_status.HTTP_401_UNAUTHORIZED)

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

        self.common_api_response_tests(response)
        self.assertEqual(
            self.UserModel.objects.first().profile.preferences.theme, "")

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
