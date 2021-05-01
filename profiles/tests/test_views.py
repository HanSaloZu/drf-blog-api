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

        self._common_api_response_tests(response)
        user = self.UserModel.objects.get(id=1)
        self.assertEqual(user.profile.status, "Test")

    def test_status_update_with_blank_value(self):
        response = self.client.put(
            self.url, {"status": ""}, content_type="application/json")

        self._common_api_response_tests(response)
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
        self.assertEqual(response.data["messages"]
                         [0], "Max Status length is 300 symbols")

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


class ProfilePhotoUpdateViewTest(APIViewTestCase):
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
