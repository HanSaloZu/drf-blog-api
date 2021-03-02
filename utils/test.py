from django.test import TestCase
from rest_framework import status
from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()

    def _create_user(self, login, email, password, is_superuser):
        if is_superuser:
            return self.UserModel.objects.create_superuser(
                login=login, email=email, password=password, is_superuser=True, is_staff=True)

        return self.UserModel.objects.create_user(
            login=login, email=email, password=password)


class ViewTestCase(ExtendedTestCase):
    request_factory = RequestFactory()
    client = Client()

    def _common_view_tests(self, response, status=status.HTTP_200_OK, result_code=0, messages_list_len=0, fields_errors_list_len=0):
        self.assertEqual(response.status_code, status)
        self.assertEqual(response.data["resultCode"], result_code)
        self.assertEqual(len(response.data["messages"]), messages_list_len)
        self.assertEqual(
            len(response.data["fieldsErrors"]), fields_errors_list_len)
