from utils.test import ExtendedTestCase

from profiles.models import Profile, Contacts, Photos


class ProfileModelTests(ExtendedTestCase):
    ProfileModel = Profile

    def setUp(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass", is_superuser=False)
        self.profile = user.profile

    def test_profile_instance(self):
        self.assertTrue(isinstance(self.profile, self.ProfileModel))

    def test_profile_data(self):
        profile = self.profile
        user = profile.user

        self.assertEqual(profile.fullname, user.login)

        self.assertEqual(profile.looking_for_a_job, False)
        self.assertEqual(profile.looking_for_a_job_description, None)

        self.assertEqual(profile.status, "")
        self.assertEqual(profile.about_me, None)


class ContactsModelTests(ExtendedTestCase):
    ContactsModel = Contacts

    def setUp(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass", is_superuser=False)
        self.contacts = user.profile.contacts

    def test_contacts_instance(self):
        self.assertTrue(isinstance(self.contacts, self.ContactsModel))

    def test_contacts_data(self):
        contacts = self.contacts

        self.assertEqual(contacts.vk, None)
        self.assertEqual(contacts.github, None)


class PhotosModelTests(ExtendedTestCase):
    PhotosModel = Photos

    def setUp(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass", is_superuser=False)
        self.photos = user.profile.photos

    def test_photos_instance(self):
        self.assertTrue(isinstance(self.photos, self.PhotosModel))

    def test_photos_data(self):
        photos = self.photos

        self.assertEqual(photos.small, None)
        self.assertEqual(photos.large, None)
