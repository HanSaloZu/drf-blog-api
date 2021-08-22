from django.urls import reverse
from urllib.parse import urlencode

from utils.tests import ListAPIViewTestCase

from ..services import ban


class ListBannedUsersAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("bans_list")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        admin_credentials = {"email": "admin@gmail.com", "password": "pass"}
        self.admin = self.UserModel.objects.create_superuser(
            login="Admin", **admin_credentials)
        self.client.login(**admin_credentials)

        self.common_user_credentials = {
            "email": "user@gmail.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="User", **self.common_user_credentials)

        first_banned_user = self.UserModel.objects.create_user(
            login="BannedUser1", email="buser1@gmail.com", password="pass")
        second_banned_user = self.UserModel.objects.create_user(
            login="BannedUser2", email="buser2@gmail.com", password="pass")
        self.first_ban = ban(receiver=first_banned_user,
                             creator=self.admin, reason="First ban")
        self.second_ban = ban(receiver=second_banned_user,
                              creator=self.admin, reason="Second ban")

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    def test_request_by_common_user(self):
        self.client.logout()
        self.client.login(**self.common_user_credentials)
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
