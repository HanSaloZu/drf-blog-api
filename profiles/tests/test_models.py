from utils.tests import ExtendedTestCase

from profiles.models import Profile, Contacts, Avatar, Banner


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


class AvatarModelTestCase(ExtendedTestCase):
    model = Avatar

    def test_avatar_model(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        avatar = user.profile.avatar

        self.assertIsInstance(avatar, self.model)

        self.assertEqual(avatar.file_id, "")
        self.assertEqual(avatar.link, "")


class BannerModelTestCase(ExtendedTestCase):
    model = Banner

    def test_banner_model(self):
        user = self.UserModel.objects.create_user(
            login="NewUser", email="new@user.com", password="pass")
        banner = user.profile.banner

        self.assertIsInstance(banner, self.model)

        self.assertEqual(banner.file_id, "")
        self.assertEqual(banner.link, "")
