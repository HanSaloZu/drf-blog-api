from django.urls import reverse

from utils.test import APIViewTestCase


class UserAuthenticationAPIViewTest(APIViewTestCase):
    url = reverse("authentication")

    def setUp(self):
        self.login_credentials = {"email": "new@user.com", "password": "pass"}
        self.registration_credentials = {"login": "RegUser", "email": "conswintcomin@gmail.com",
                                         "password1": "pass", "password2": "pass", "aboutMe": "About Me!"}
        self.user = self.UserModel.objects.create_user(
            login="NewUser", **self.login_credentials)

    # Authorization testing

    def test_authentication_with_valid_data(self):
        response = self.client.put(
            self.url, self.login_credentials, content_type="application/json")

        self.common_api_response_tests(response)
        self.assertEqual(response.data["data"]["userId"], self.user.id)

    def test_authentication_with_invalid_email(self):
        response = self.client.put(
            self.url, {
                "email": "123",
                "password": self.login_credentials["password"]
            }, content_type="application/json")

        self.common_api_response_tests(
            response, result_code=1, messages_list_len=1, fields_errors_list_len=1, messages=["Enter valid Email"])

    def test_authentication_with_invalid_password(self):
        response = self.client.put(
            self.url, {
                "email": self.login_credentials["email"],
                "password": "invalid"
            }, content_type="application/json")

        self.common_api_response_tests(response, result_code=1,
                                       messages_list_len=1, fields_errors_list_len=0, messages=["Incorrect Email or Password"])

    def test_authentication_wihout_credentials(self):
        response = self.client.put(self.url)

        self.common_api_response_tests(response, result_code=1, messages_list_len=2, fields_errors_list_len=2, messages=[
            "Please enter your Email", "Enter your password"])

    # Logging out testing

    def test_logging_out(self):
        self.client.login(**self.login_credentials)
        response = self.client.delete(self.url)
        self.common_api_response_tests(response)

    def test_unauthorized_logging_out(self):
        response = self.client.delete(self.url)
        self.common_api_response_tests(response)
