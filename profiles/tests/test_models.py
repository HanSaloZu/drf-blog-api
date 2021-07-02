from utils.tests import ExtendedTestCase

from profiles.models import Profile, Contacts, Photo, Preferences


class ProfileModelTest(ExtendedTestCase):
    model = Profile

    def test_profile(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        profile = user.profile

        self.assertIsInstance(profile, self.model)

        self.assertFalse(profile.is_looking_for_a_job)
        self.assertEqual(profile.professional_skills, "")

        self.assertEqual(profile.fullname, user.login)
        self.assertEqual(profile.status, "")
        self.assertEqual(profile.about_me, "")


class ContactsModelTest(ExtendedTestCase):
    model = Contacts

    def test_contacts(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        contacts = user.profile.contacts

        self.assertIsInstance(contacts, self.model)

        self.assertEqual(contacts.vk, "")
        self.assertEqual(contacts.github, "")
        self.assertEqual(contacts.facebook, "")
        self.assertEqual(contacts.instagram, "")
        self.assertEqual(contacts.main_link, "")
        self.assertEqual(contacts.twitter, "")
        self.assertEqual(contacts.website, "")
        self.assertEqual(contacts.youtube, "")


class PhotoModelTest(ExtendedTestCase):
    model = Photo

    def test_photo(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        photo = user.profile.photo

        self.assertIsInstance(photo, self.model)

        self.assertEqual(photo.file_id, "")
        self.assertEqual(photo.link, "")


class PreferencesModelTest(ExtendedTestCase):
    model = Preferences

    def test_preferences(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        preferences = user.profile.preferences

        self.assertIsInstance(preferences, self.model)

        self.assertEqual(preferences.theme, "")
