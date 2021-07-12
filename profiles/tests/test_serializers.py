from django.utils.crypto import get_random_string
from django.test import TestCase

from utils.shortcuts import generate_messages_list_by_serializer_errors
from utils.tests import ExtendedTestCase

from ..serializers import (UpdateProfileSerializer, UpdateContactsSerializer, UpdatePasswordSerailizer,
                           PreferencesSerializer, ProfileSerializer)


class ProfileSerializerTestCase(ExtendedTestCase):
    serializer_class = ProfileSerializer

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")

    def test_serializer_with_instance(self):
        instance = self.user.profile
        serializer = self.serializer_class(instance=instance)
        data = serializer.data

        self.assertEqual(len(data), 10)
        self.assertEqual(data["userId"], instance.user.id)
        self.assertEqual(data["isLookingForAJob"],
                         instance.is_looking_for_a_job)
        self.assertEqual(data["professionalSkills"],
                         instance.professional_skills)
        self.assertEqual(data["isAdmin"], instance.user.is_staff)
        self.assertEqual(data["fullname"], instance.fullname)
        self.assertEqual(data["login"], instance.user.login)
        self.assertEqual(data["aboutMe"], instance.about_me)
        self.assertEqual(data["status"], instance.status)
        self.assertEqual(data["photo"], instance.photo.link)

        self.assertEqual(len(data["contacts"]), 8)
        self.assertEqual(data["contacts"]
                         ["github"], instance.contacts.github)
        self.assertEqual(data["contacts"]
                         ["facebook"], instance.contacts.facebook)
        self.assertEqual(data["contacts"]
                         ["instagram"], instance.contacts.instagram)
        self.assertEqual(data["contacts"]
                         ["mainLink"], instance.contacts.main_link)
        self.assertEqual(data["contacts"]
                         ["twitter"], instance.contacts.twitter)
        self.assertEqual(data["contacts"]["vk"], instance.contacts.vk)
        self.assertEqual(data["contacts"]
                         ["website"], instance.contacts.website)
        self.assertEqual(data["contacts"]
                         ["youtube"], instance.contacts.youtube)


class UpdateProfileSerializerTestCase(TestCase):
    serializer_class = UpdateProfileSerializer

    def test_valid_serializer(self):
        data = {
            "fullname": "New User",
            "aboutMe": get_random_string(length=70),
            "isLookingForAJob": True,
            "professionalSkills": "Backend web developer",
            "status": "New status"
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)

    def test_invalid_serializer(self):
        data = {
            "fullname": "",
            "aboutMe": get_random_string(length=69),
            "status": get_random_string(length=100),
            "professionalSkills": None,
            "isLookingForAJob": "invalid",
            "contacts": None
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Fullname field cannot be empty", errors)
        self.assertIn("About me field value is too short", errors)
        self.assertIn("Status field value is too long", errors)
        self.assertIn("Professional skills field cannot be null", errors)
        self.assertIn("Invalid value for is looking for a job field", errors)
        self.assertIn("Contacts field cannot be null", errors)
        self.assertEqual(len(errors), 6)


class UpdateContactsSerializerTestCase(TestCase):
    serializer_class = UpdateContactsSerializer

    def test_valid_serializer(self):
        data = {
            "github": "https://github.com/HanSaloZu",
            "twitter": ""
        }
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)

    def test_invalid_serializer(self):
        data = {
            "github": "123",
            "twitter": None,
            "facebook": get_random_string(length=205),
            "vk": ""
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Invalid value for github field", errors)
        self.assertIn("Twitter field cannot be null", errors)
        self.assertIn("Facebook field value is too long", errors)
        self.assertEqual(len(errors), 3)


class UpdatePasswordSerializerTestCase(TestCase):
    serializer_class = UpdatePasswordSerailizer

    def test_invalid_serializer(self):
        data = {
            "oldPassword": "pass",
            "newPassword1": "",
            "newPassword2": None
        }
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("New password field cannot be empty", errors)
        self.assertIn("Repeat new password field cannot be null", errors)
        self.assertEqual(len(errors), 2)

    def test_serializer_without_data(self):
        serializer = self.serializer_class(data={})

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Old password field is required", errors)
        self.assertIn("New password field is required", errors)
        self.assertIn("Repeat new password field is required", errors)
        self.assertEqual(len(errors), 3)


class PreferencesSerializerTestCase(TestCase):
    serializer_class = PreferencesSerializer

    def test_valid_serializer(self):
        data = {"theme": ""}
        serializer = self.serializer_class(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(data, serializer.validated_data)

    def test_invalid_serializer(self):
        data = {"theme": "a"*260}
        serializer = self.serializer_class(data=data)

        self.assertFalse(serializer.is_valid())

        errors = generate_messages_list_by_serializer_errors(serializer.errors)
        self.assertIn("Theme field value is too long", errors)
        self.assertEqual(len(errors), 1)

    def test_serializer_without_data(self):
        serializer = self.serializer_class(data={})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors["theme"][0], "Theme field is required")
