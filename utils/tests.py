from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


class ExtendedTestCase(APITestCase):
    UserModel = get_user_model()


class APIViewTestCase(ExtendedTestCase):
    http_status = status

    def generate_jwt_auth_credentials(self, user):
        token = RefreshToken.for_user(user).access_token
        return "JWT {0}".format(token)

    def client_error_response_test(self, response,
                                   code="invalid",
                                   status=http_status.HTTP_400_BAD_REQUEST,
                                   messages_list_len=0,
                                   fields_errors_dict_len=0,
                                   messages=[]):

        def calc_number_of_fields_errors(fields_errors):
            counter = len(fields_errors)

            for field in fields_errors:
                # If the field error value is dict, then
                # it is a group of fields

                if isinstance(fields_errors[field], dict):
                    # Groups of fields are not counted in the counter,
                    # so 1 is subtracted from the counter
                    counter += calc_number_of_fields_errors(
                        fields_errors[field]
                    ) - 1

            return counter

        if messages_list_len == 0 and len(messages) != 0:
            messages_list_len = len(messages)

        self.assertEqual(response.status_code, status)
        self.assertEqual(response.data["code"], code)
        self.assertEqual(len(response.data["messages"]), messages_list_len)
        self.assertEqual(
            calc_number_of_fields_errors(response.data["fieldsErrors"]),
            fields_errors_dict_len
        )

        for m in messages:
            self.assertIn(m, response.data["messages"])

    def unauthorized_client_error_response_test(self, response):
        self.client_error_response_test(
            response,
            code="notAuthenticated",
            status=self.http_status.HTTP_401_UNAUTHORIZED,
            messages=["You are not authenticated"],
            fields_errors_dict_len=0
        )


class ListAPIViewTestCase(APIViewTestCase):
    def check_common_details_of_list_view_response(self, response,
                                                   total_items=0,
                                                   total_pages=1,
                                                   page_size=0,
                                                   page_number=1):
        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(len(response.data["items"]), page_size)
        self.assertEqual(response.data["totalItems"], total_items)
        self.assertEqual(response.data["totalPages"], total_pages)
        self.assertEqual(response.data["pageSize"], page_size)
        self.assertEqual(response.data["pageNumber"], page_number)
