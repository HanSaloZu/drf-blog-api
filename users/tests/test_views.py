from django.urls import reverse

from utils.test import ViewTestCase
from users.views import user_detail


class UserDetailViewTest(ViewTestCase):
    def setUp(self):
        self.user = self._create_user(login="NewUser", email="new@user.com",
                                      password="pass", is_superuser=False)
        self.url = reverse("user_detail")

    def test_invalid_user_detail(self):
        response = self.client.get(self.url)

        self._common_view_tests(response, result_code=1, messages_list_len=1)
        message = response.data["messages"][0]
        self.assertEqual(message, "You are not authorized")

    def test_valid_user_detail(self):
        user = self.user
        request = self.request_factory.get(self.url)
        request.user = user
        response = user_detail(request)

        self._common_view_tests(response)
        response_user_data = response.data["data"]
        self.assertEqual(response_user_data["id"], user.id)
        self.assertEqual(response_user_data["login"], user.login)
        self.assertEqual(response_user_data["email"], user.email)
