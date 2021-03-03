from django.urls import reverse
from rest_framework import status
import json

from utils.test import ViewTestCase


class ProfileStatusDetailViewTest(ViewTestCase):
    def setUp(self):
        self.user = self._create_user(login="NewUser", email="new@user.com",
                                      password="pass", is_superuser=False)

    def test_invalid_status_detail(self):
        url = reverse("profile_status_detail", kwargs={"user_id": 9})
        response = self.client.get(url)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data["message"], "An error has occurred.")

    def test_valid_status_detail(self):
        def common_status_detail_view_tests(response):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json.loads(response.content),
                             self.user.profile.status)

        url = reverse("profile_status_detail", kwargs={"user_id": 1})
        common_status_detail_view_tests(self.client.get(url))

        self.user.profile.status = "test"
        self.user.save()
        common_status_detail_view_tests(self.client.get(url))


class ProfileDetailViewTest(ViewTestCase):
    def setUp(self):
        user = self._create_user(login="NewUser", email="new@user.com",
                                 password="pass", is_superuser=False)
        profile = user.profile

        profile.looking_for_a_job = True
        profile.looking_for_a_job_description = "Test"
        profile.about_me = "I am a view test"
        profile.contacts.github = "https://github.com/HanSaloZu"
        user.save()
        self.profile = profile

    def test_valid_profile_detail(self):
        url = reverse("profile_detail", kwargs={"user_id": 1})
        response = self.client.get(url)
        data = response.data
        profile = self.profile

        self.assertEqual(data["userId"], profile.user.id)
        self.assertEqual(data["lookingForAJob"], True)
        self.assertEqual(data["lookingForAJobDescription"],
                         profile.looking_for_a_job_description)
        self.assertEqual(data["fullName"], profile.fullname)
        self.assertEqual(data["aboutMe"], profile.about_me)
        self.assertEqual(len(data["contacts"]), 8)
        self.assertEqual(data["contacts"]["github"], profile.contacts.github)
        self.assertEqual(len(data["photos"]), 2)

    def test_invalid_profile_detail(self):
        url = reverse("profile_detail", kwargs={"user_id": 9})
        response = self.client.get(url)

        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
