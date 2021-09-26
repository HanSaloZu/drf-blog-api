from django.urls import reverse
from urllib.parse import urlencode
from django.utils.crypto import get_random_string

from utils.tests import ListAPIViewTestCase, APIViewTestCase

from ..models import Ban
from ..services import ban


class ListBannedUsersAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("bans_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        self.admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")

        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.admin)
        )

        self.user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")

        first_banned_user = self.UserModel.objects.create_user(
            login="BannedUser1", email="buser1@gmail.com", password="pass")
        second_banned_user = self.UserModel.objects.create_user(
            login="BannedUser2", email="buser2@gmail.com", password="pass")
        self.first_ban = ban(receiver=first_banned_user,
                             creator=self.admin, reason="First ban")
        self.second_ban = ban(receiver=second_banned_user,
                              creator=self.admin, reason="Second ban")

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    def test_request_by_common_user(self):
        """
        Only administrators can access this resource.
        A request from a common user should return a 403 statuts code
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.user)
        )
        response = self.client.get(self.url())

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You don't have permission to access this resource"]
        )

    def test_bans_list(self):
        """
        A bans list request should return a list of 2 bans
        """
        response = self.client.get(self.url())

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )

    def test_bans_list_with_limit_parameter(self):
        """
        A request for a list of bans with the limit parameter
        should return a list of bans
        with the number of bans equal to the limit parameter
        """
        response = self.client.get(self.url({"limit": 1}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            total_pages=2,
            page_size=1
        )

        self.assertEqual(response.data["items"][0]["receiver"]["login"],
                         self.second_ban.receiver.login)

    def test_posts_list_with_q_parameter(self):
        """
        A bans list request with the q parameter
        should return a list of bans matching the q parameter
        """
        # Searching by reason
        response = self.client.get(self.url({"q": "First ban"}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )

        ban = response.data["items"][0]
        self.assertEqual(len(ban), 4)
        self.assertEqual(len(ban["receiver"]), 4)
        self.assertEqual(ban["receiver"]["login"],
                         self.first_ban.receiver.login)

        # Searching by receiver
        response = self.client.get(self.url({"q": "BannedUser2"}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )

        self.assertEqual(response.data["items"][0]["receiver"]["login"],
                         self.second_ban.receiver.login)

        # Searching by creator
        response = self.client.get(self.url({"q": "Admin"}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )


class BanAPIViewTestCase(APIViewTestCase):
    def url(self, kwargs):
        return reverse("ban", kwargs=kwargs)

    def setUp(self):
        self.admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="pass")

        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.admin)
        )

        self.second_admin = self.UserModel.objects.create_superuser(
            login="SecondAdmin", email="second_admin@gmail.com", password="pass")

        self.user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")

        self.banned_user = self.UserModel.objects.create_user(
            login="BannedUser", email="buser@gmail.com", password="pass")
        ban(receiver=self.banned_user, creator=self.admin, reason="Ban")

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"login": self.banned_user.login}))

        self.unauthorized_client_error_response_test(response)

    def test_request_by_common_user(self):
        """
        Only administrators can access this resource.
        A request from a common user should return a 403 statuts code
        """
        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.user)
        )
        response = self.client.get(self.url({"login": self.banned_user.login}))

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You don't have permission to access this resource"]
        )

    # Retrieve ban object

    def test_retrieve_banned_user(self):
        """
        Retrieving a banned user should return a 200 status code
        and a ban representation
        """
        response = self.client.get(self.url({"login": self.banned_user.login}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["receiver"]
                         ["login"], self.banned_user.login)

    def test_retrieve_banned_user_with_invalid_login(self):
        """
        Retrieving a banned user with an invalid login should return
        a 404 status code
        """
        response = self.client.get(self.url({"login": "invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login or user is not banned"]
        )

    # Ban

    def test_valid_banning(self):
        """
        Valid user banning should return a 201 status code
        and a ban representation
        """
        payload = {
            "reason": "Ban"
        }
        response = self.client.put(self.url({"login": self.user.login}),
                                   payload, content_type="application/json")

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_201_CREATED)
        self.assertEqual(response.data["reason"], payload["reason"])
        self.assertEqual(response.data["creator"]["login"], self.admin.login)
        self.assertEqual(response.data["receiver"]["login"], self.user.login)

    def test_admin_banning(self):
        """
        Admins cannot be banned.
        Admin banning should return a 403 status code
        """
        payload = {
            "reason": "Ban"
        }
        response = self.client.put(self.url({"login": self.second_admin.login}),
                                   payload, content_type="application/json")

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["Admins cannot be banned"]
        )

    def test_banning_user_with_invalid_login(self):
        """
        Banning a user with an invalid login should return a 404 status code
        """
        response = self.client.put(self.url({"login": "invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login, user is not found"]
        )

    def test_invalid_banning(self):
        """
        Invalid user banning should return a 400 status code
        and a list of errors
        """
        payload = {
            "reason": None
        }
        response = self.client.put(self.url({"login": self.user.login}),
                                   payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Reason cannot be null"],
            fields_errors_dict_len=1
        )

    # Update ban

    def test_valid_ban_update(self):
        """
        Valid ban updating should return a 200 status code
        and a new ban representation
        """
        payload = {
            "reason": "Updated ban reason"
        }
        response = self.client.put(self.url({"login": self.banned_user.login}),
                                   payload, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.assertEqual(response.data["reason"], payload["reason"])
        self.assertEqual(response.data["reason"],
                         Ban.objects.all().first().reason)
        self.assertEqual(response.data["receiver"]
                         ["login"], self.banned_user.login)
        self.assertEqual(response.data["creator"]["login"], self.admin.login)

    def test_invalid_ban_update(self):
        """
        Invalid ban updating should return a 400 status code
        and a list of errors
        """
        payload = {
            "reason": get_random_string(length=300)
        }
        response = self.client.put(self.url({"login": self.banned_user.login}),
                                   payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=["Reason must be up to 250 characters long"],
            fields_errors_dict_len=1
        )

    # Unban

    def test_valid_unbanning(self):
        """
        Valid user unbanning should return a 204 status code
        """
        response = self.client.delete(
            self.url({"login": self.banned_user.login}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Ban.objects.all().exists())

    def test_unbanning_user_with_invalid_login(self):
        """
        Unbanning a user with an invalid login should return a 404 status code
        """
        response = self.client.delete(self.url({"login": "invalid"}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid login or user is not banned"]
        )
