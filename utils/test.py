from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()


class APIViewTestCase(ExtendedTestCase):
    client = APIClient()
    http_status = status

    def _common_api_response_tests(self, response, status=http_status.HTTP_200_OK, result_code=0, messages_list_len=0, fields_errors_list_len=0, messages=[]):
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.data["resultCode"], result_code)
        self.assertEqual(len(response.data["messages"]), messages_list_len)
        self.assertEqual(
            len(response.data["fieldsErrors"]), fields_errors_list_len)

        for m in messages:
            self.assertIn(m, messages)
