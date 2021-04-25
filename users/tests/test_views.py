from django.urls import reverse

from utils.test import APIViewTestCase
from users.views import UserDetail


class UserDetailAPIViewTest(APIViewTestCase):
    url = reverse("user_detail")

    def test_unauthorized_user_request_user_detail(self):
        response = self.client.get(self.url)

        self._common_api_response_tests(
            response, result_code=1, messages_list_len=1)
        message = response.data["messages"][0]
        self.assertEqual(message, "You are not authorized")

    def test_valid_user_detail(self):
        user = self._create_user(
            login="NewUser", email="new@user.com", password="pass")
        request = self.request_factory.get(self.url)
        view = UserDetail()

        request.user = user
        view.setup(request)
        response = view.get(request)

        self._common_api_response_tests(response)
        response_user_detail = response.data["data"]
        self.assertEqual(response_user_detail["id"], user.id)
        self.assertEqual(response_user_detail["login"], user.login)
        self.assertEqual(response_user_detail["email"], user.email)


class UserAuthenticationAPIViewTest(APIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.login = "NewUser"
        self.email = "new@user.com"
        self.password = "pass"
        self.user = self._create_user(login=self.login, email=self.email,
                                      password=self.password)

    def tearDown(self):
        self.user.delete()

    def test_authentication_with_valid_data(self):
        response = self.client.post(
            self.url, {
                "email": self.email,
                "password": self.password
            })

        self._common_api_response_tests(response)
        self.assertEqual(response.data["data"]["userId"], self.user.id)

    def test_authentication_with_invalid_email(self):
        response = self.client.post(
            self.url, {
                "email": "123",
                "password": self.password
            })

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=1, fields_errors_list_len=1)
        self.assertEqual(response.data["messages"][0], "Enter valid Email")
        self.assertEqual(response.data["fieldsErrors"][0]["field"], "email")
        self.assertEqual(response.data["fieldsErrors"]
                         [0]["error"], "Enter valid Email")

    def test_authentication_with_invalid_password(self):
        response = self.client.post(
            self.url, {
                "email": self.user.email,
                "password": "invalid"
            })

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=1, fields_errors_list_len=0)
        self.assertEqual(response.data["messages"]
                         [0], "Incorrect Email or Password")

    def test_authentication_wihout_credentials(self):
        response = self.client.post(self.url)

        self._common_api_response_tests(response, result_code=1,
                                        messages_list_len=2, fields_errors_list_len=2)
        self.assertIn("Please enter your Email", response.data["messages"])
        self.assertIn("Enter your password", response.data["messages"])

    def test_logging_out(self):
        self.client.post(
            self.url, {
                "email": self.user.email,
                "password": self.password
            })
        response = self.client.delete(self.url)
        self._common_api_response_tests(response)

    def test_unauthorized_logging_out(self):
        response = self.client.delete(self.url)
        self._common_api_response_tests(response)
