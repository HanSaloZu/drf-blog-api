from django.utils.crypto import get_random_string
from django.urls import reverse

from utils.tests import APIViewTestCase
from posts.models import Post, Like


class RetrieveUpdateProfileAPIViewTestCase(APIViewTestCase):
    url = reverse("profile")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)

        user.profile.is_looking_for_a_job = True
        user.profile.professional_skills = "Test"
        user.profile.about_me = "I am a view test"
        user.profile.contacts.github = "https://github.com/HanSaloZu"
        user.save()

        self.user = user
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url)

        self.unauthorized_client_error_response_test(response)

    # Profile retrieving tests

    def test_profile_detail(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    # Profile update tests

    def test_profile_update_without_contacts(self):
        """
        Profile update without contacts is valid
        and should return a 200 status code and a profile representation
        """
        payload = {
            "fullname": "New User",
            "aboutMe": get_random_string(length=70),
            "isLookingForAJob": True,
            "professionalSkills": "Backend web developer",
            "status": "New status",
            "theme": "dark",
            "location": "Berlin",
            "birthday": "2000-01-19"
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")
        user = self.UserModel.objects.all().first()

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.about_me, payload["aboutMe"])
        self.assertEqual(user.profile.status, payload["status"])
        self.assertEqual(user.profile.theme, payload["theme"])
        self.assertEqual(str(user.profile.birthday), payload["birthday"])
        self.assertEqual(user.profile.location, payload["location"])

        self.assertEqual(user.profile.is_looking_for_a_job,
                         payload["isLookingForAJob"])
        self.assertEqual(user.profile.professional_skills,
                         payload["professionalSkills"])

    def test_profile_update_with_contacts(self):
        """
        Valid profile update should return a 200 status code
        and a profile representation in the response body
        """
        payload = {
            "fullname": "New Fullname",
            "status": "",
            "contacts": {
                "github": "https://github.com/HanSaloZu",
                "mainLink": "https://github.com/HanSaloZu",
                "twitter": ""
            }
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")
        user = self.UserModel.objects.all().first()
        contacts = user.profile.contacts

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], user.id)

        self.assertEqual(user.profile.fullname, payload["fullname"])
        self.assertEqual(user.profile.status, payload["status"])

        self.assertEqual(contacts.github, payload["contacts"]["github"])
        self.assertEqual(contacts.main_link, payload["contacts"]["mainLink"])
        self.assertEqual(contacts.twitter, payload["contacts"]["twitter"])
        self.assertEqual(contacts.facebook,
                         self.user.profile.contacts.facebook)

    def test_profile_update_without_payload(self):
        """
        Profile update without payload is valid
        and should return a 200 status code and a profile representation
        """
        response = self.client.patch(self.url)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)

    def test_profile_update_with_invalid_payload(self):
        """
        Profile update with invalid payload should return a 400 status code
        """
        payload = {
            "fullname": "",
            "location": "a"*290,
            "aboutMe": "a"*802,
            "theme": None,
            "contacts": {
                "github": "123",
            }
        }
        response = self.client.patch(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=[
                "Fullname field cannot be empty",
                "Location field value is too long",
                "About me field value is too long",
                "Theme field cannot be null",
                "Invalid value for github field"
            ],
            fields_errors_dict_len=5
        )


class UpdateAvatarAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_avatar_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_avatar_update_without_payload(self):
        """
        Avatar update without payload should return a 400 error
        """
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )

    def test_avatar_update_with_invalid_payload(self):
        """
        Avatar update with invalid payload should return a 400 error
        """
        response = self.client.put(
            self.url,
            {"avatar": "test"},
            content_type="multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW")

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )


class UpdateBannerAPIViewTestCase(APIViewTestCase):
    url = reverse("profile_banner_update")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_banner_update_without_payload(self):
        """
        Banner update without payload should return a 400 error
        """
        response = self.client.put(self.url)

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )

    def test_banner_update_with_invalid_payload(self):
        """
        Banner update with invalid payload should return a 400 error
        """
        response = self.client.put(
            self.url,
            {"banner": "test"},
            content_type="multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW")

        self.client_error_response_test(
            response,
            messages=[
                "File not provided",
            ],
            fields_errors_dict_len=1
        )


class UpdatePasswordAPIViewTestCase(APIViewTestCase):
    url = reverse("update_password")

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)

        self.client.login(**credentials)

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.put(self.url)

        self.unauthorized_client_error_response_test(response)

    def test_update_password(self):
        """
        Valid password update should return a 204 status code
        """
        payload = {
            "oldPassword": "pass",
            "newPassword1": "newpassword",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)

        user = self.UserModel.objects.all().first()
        self.assertIs(user.check_password(payload["newPassword1"]), True)

    def test_update_password_with_different_passwords(self):
        """
        Password update with different passwords should return a 400 error
        """
        payload = {
            "oldPassword": "pass",
            "newPassword1": "invalid",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Passwords do not match"],
            fields_errors_dict_len=1
        )

    def test_update_password_with_invalid_current_password(self):
        """
        Password update with invalid current password should return a 400 error
        """
        payload = {
            "oldPassword": "invalid",
            "newPassword1": "newpassword",
            "newPassword2": "newpassword"
        }
        response = self.client.put(
            self.url, payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Invalid password"],
            fields_errors_dict_len=1
        )


class RetrieveCreateDestroyLikedPostAPIViewTestCase(APIViewTestCase):
    def url(self, kwargs):
        return reverse("liked_posts", kwargs=kwargs)

    def setUp(self):
        credentials = {"email": "new@user.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **credentials)
        self.client.login(**credentials)

        self.first_post = Post.objects.create(
            author=self.user, title="First post")
        self.second_post = Post.objects.create(
            author=self.user, title="Second post")

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url({"id": self.first_post.id}))

        self.unauthorized_client_error_response_test(response)

    # Check if is liked

    def test_check_if_post_is_liked(self):
        """
        Checking if post is liked should return a 200 status code
        and isLiked flag
        """
        # not liked
        response = self.client.get(self.url({"id": self.first_post.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isLiked"], False)

        # liked
        Like.objects.create(post=self.second_post, user=self.user)

        response = self.client.get(self.url({"id": self.second_post.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isLiked"], True)

    def test_check_if_post_is_liked_with_invalid_id(self):
        """
        Checking if post is liked with invalid id
        should return a 404 status code
        """
        response = self.client.get(self.url({"id": 99}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )

    # Like post

    def test_like_post(self):
        """
        Post liking should return a 200 status code
        and isLiked: True
        """
        response = self.client.put(self.url({"id": self.first_post.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isLiked"], True)
        self.assertTrue(Like.objects.filter(
            post=self.first_post,
            user=self.user
        ).exists())

    def test_like_post_with_invalid_id(self):
        """
        Liking post with invalid id should return a 404 status code
        """
        response = self.client.put(self.url({"id": 99}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )

    # Unlike post

    def test_unlike_post(self):
        """
        Post unliking should return a 200 status code
        and isLiked: False
        """
        Like.objects.create(post=self.second_post, user=self.user)
        response = self.client.delete(self.url({"id": self.second_post.id}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertIs(response.data["isLiked"], False)
        self.assertFalse(Like.objects.filter(
            post=self.second_post,
            user=self.user
        ).exists())

    def test_unlike_post_with_invalid_id(self):
        """
        Unliking post with invalid id should return a 404 status code
        """
        response = self.client.delete(self.url({"id": 99}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )
