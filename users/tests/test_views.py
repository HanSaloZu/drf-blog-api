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


class UserAuthenticationViewTest(ViewTestCase):
    def setUp(self):
        self.user = self._create_user(login="NewUser", email="new@user.com",
                                      password="pass", is_superuser=False)
        self.url = reverse("authentication")

    def tearDown(self):
        self.client.delete(self.url)  # logout

    def test_valid_logging_in(self):
        def local_common_tests(response):
            self._common_view_tests(response)
            response_user_id = response.data["data"]["userId"]
            self.assertEqual(response_user_id, self.user.id)

        response = self.client.post(
            self.url, {
                "email": self.user.email,
                "password": "pass"
            })
        local_common_tests(response)

        response = self.client.post(
            self.url, {
                "email": self.user.email,
                "password": "pass",
                "rememberMe": True
            })
        local_common_tests(response)

    def test_invalid_logging_in(self):
        response = self.client.post(
            self.url, {
                "email": "123",
                "password": "pass"
            })

        self._common_view_tests(response, result_code=1,
                                messages_list_len=1, fields_errors_list_len=1)
        self.assertEqual(response.data["messages"][0], "Enter valid Email")
        self.assertEqual(response.data["fieldsErrors"][0]["field"], "email")
        self.assertEqual(response.data["fieldsErrors"]
                         [0]["error"], "Enter valid Email")

        response = self.client.post(
            self.url, {
                "email": self.user.email,
                "password": "invalid"
            })

        self._common_view_tests(response, result_code=1,
                                messages_list_len=1, fields_errors_list_len=0)
        self.assertEqual(response.data["messages"]
                         [0], "Incorrect Email or Password")

        response = self.client.post(self.url)
        self._common_view_tests(response, result_code=1,
                                messages_list_len=2, fields_errors_list_len=2)

        response = self.client.post(
            self.url, {
                "email": self.user.email,
                "password": "invalid",
                "rememberMe": "123"
            })

        self._common_view_tests(response, result_code=1,
                                messages_list_len=1, fields_errors_list_len=1)
        self.assertEqual(response.data["messages"]
                         [0], "Invalid value for rememberMe")

    def test_logging_out(self):
        response = self.client.delete(self.url)
        self._common_view_tests(response)
