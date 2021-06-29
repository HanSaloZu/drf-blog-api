from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()


class APIViewTestCase(ExtendedTestCase):
    client = APIClient()
    http_status = status

    def client_error_response_test(self, response, code=None,
                                   status=http_status.HTTP_400_BAD_REQUEST, messages_list_len=0, fields_errors_dict_len=0, messages=[]):
        if not code is None:
            self.assertEqual(response.data["code"], code)

        self.assertEqual(response.status_code, status)
        self.assertEqual(len(response.data["messages"]), messages_list_len)
        self.assertEqual(
            len(response.data["fieldsErrors"]), fields_errors_dict_len)

        for m in messages:
            self.assertIn(m, response.data["messages"])
