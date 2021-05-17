from utils.test import ExtendedTestCase

from ..models import Profile, Contacts, Photo, ProfilePreferences


class ProfileModelTest(ExtendedTestCase):
    model = Profile

    def test_profile(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        profile = user.profile

        self.assertIsInstance(profile, self.model)

        self.assertEqual(profile.fullname, user.login)

        self.assertFalse(profile.looking_for_a_job)
        self.assertIsNone(profile.looking_for_a_job_description)

        self.assertEqual(profile.status, "")
        self.assertIsNone(profile.about_me)


class ContactsModelTest(ExtendedTestCase):
    model = Contacts

    def test_contacts(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        contacts = user.profile.contacts

        self.assertIsInstance(contacts, self.model)

        self.assertIsNone(contacts.vk)
        self.assertIsNone(contacts.github)
        self.assertIsNone(contacts.facebook)
        self.assertIsNone(contacts.instagram)
        self.assertIsNone(contacts.main_link)
        self.assertIsNone(contacts.twitter)
        self.assertIsNone(contacts.website)
        self.assertIsNone(contacts.youtube)


class PhotoModelTest(ExtendedTestCase):
    model = Photo

    def test_photo(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        photo = user.profile.photo

        self.assertIsInstance(photo, self.model)

        self.assertIsNone(photo.file_id)
        self.assertIsNone(photo.link)


class ProfilePreferencesModelTest(ExtendedTestCase):
    model = ProfilePreferences

    def test_preferences(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        preferences = user.profile.preferences

        self.assertIsInstance(preferences, self.model)
        self.assertEqual(preferences.theme, "")
