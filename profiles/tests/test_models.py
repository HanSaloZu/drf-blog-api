from utils.test import ExtendedTestCase

from profiles.models import Profile, Contacts, Photo


class ProfileModelTest(ExtendedTestCase):
    model = Profile

    def test_profile(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass")
        profile = user.profile

        self.assertIsInstance(profile, self.model)

        self.assertEqual(profile.fullname, user.login)

        self.assertFalse(profile.looking_for_a_job)
        self.assertIsNone(profile.looking_for_a_job_description)

        self.assertEqual(profile.status, "")
        self.assertIsNone(profile.about_me)


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


class PhotoModelTests(ExtendedTestCase):
    PhotoModel = Photo

    def setUp(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass", is_superuser=False)
        self.photo = user.profile.photo

    def test_photos_instance(self):
        self.assertTrue(isinstance(self.photo, self.PhotoModel))

    def test_photos_data(self):
        photo = self.photo

        self.assertEqual(photo.file_id, None)
        self.assertEqual(photo.link, None)
