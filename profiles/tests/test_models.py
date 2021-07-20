from utils.tests import ExtendedTestCase

from profiles.models import Profile, Contacts, Photo, Preferences


class ProfileModelTestCase(ExtendedTestCase):
    model = Profile

    def test_profile_model(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        profile = user.profile

        self.assertIsInstance(profile, self.model)

        self.assertIs(profile.is_looking_for_a_job, False)
        self.assertEqual(profile.professional_skills, "")

        self.assertEqual(profile.fullname, user.login)
        self.assertEqual(profile.status, "")
        self.assertEqual(profile.about_me, "")
        self.assertEqual(profile.location, "")
        self.assertIsNone(profile.birthday)


class ContactsModelTestCase(ExtendedTestCase):
    model = Contacts

    def test_contacts_model(self):
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


class PhotoModelTestCase(ExtendedTestCase):
    model = Photo

    def test_photo_model(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        photo = user.profile.photo

        self.assertIsInstance(photo, self.model)

        self.assertEqual(photo.file_id, "")
        self.assertEqual(photo.link, "")


class PreferencesModelTestCase(ExtendedTestCase):
    model = Preferences

    def test_preferences_model(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        preferences = user.profile.preferences

        self.assertIsInstance(preferences, self.model)

        self.assertEqual(preferences.theme, "")
