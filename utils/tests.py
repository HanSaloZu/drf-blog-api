from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class ExtendedTestCase(TestCase):
    UserModel = get_user_model()


class APIViewTestCase(ExtendedTestCase):
    client = APIClient()
    http_status = status

    def client_error_response_test(self, response,
                                   code=None,
                                   status=http_status.HTTP_400_BAD_REQUEST,
                                   messages_list_len=0,
                                   fields_errors_dict_len=0,
                                   messages=[]):

        def calc_number_of_fields_errors(fields_errors):
            counter = len(fields_errors)

            for field in fields_errors:
                # If the field error value is dict, then this is a group of fields

                if isinstance(fields_errors[field], dict):
                    # Groups of fields are not counted in the counter, so 1 is subtracted from the counter

                    counter += calc_number_of_fields_errors(
                        fields_errors[field]) - 1

            return counter

        if not code is None:
            self.assertEqual(response.data["code"], code)

        self.assertEqual(response.status_code, status)
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
            messages_list_len=1,
            messages=["You are not authenticated"],
            fields_errors_dict_len=0
        )


class ProfileDetailAPIViewTestCase(APIViewTestCase):
    def compare_profile_instance_and_response_data(self, profile, response):
        self.assertEqual(response["userId"], profile.user.id)
        self.assertEqual(response["isLookingForAJob"],
                         profile.is_looking_for_a_job)
        self.assertEqual(response["professionalSkills"],
                         profile.professional_skills)
        self.assertEqual(response["fullname"], profile.fullname)
        self.assertEqual(response["aboutMe"], profile.about_me)
        self.assertEqual(response["status"], profile.status)
        self.assertEqual(len(response["contacts"]), 8)
        self.assertEqual(response["photo"], profile.photo.link)
        self.assertEqual(response["contacts"]
                         ["github"], profile.contacts.github)
        self.assertEqual(response["contacts"]
                         ["facebook"], profile.contacts.facebook)
        self.assertEqual(response["contacts"]
                         ["instagram"], profile.contacts.instagram)
        self.assertEqual(response["contacts"]
                         ["mainLink"], profile.contacts.main_link)
        self.assertEqual(response["contacts"]
                         ["twitter"], profile.contacts.twitter)
        self.assertEqual(response["contacts"]["vk"], profile.contacts.vk)
        self.assertEqual(response["contacts"]
                         ["website"], profile.contacts.website)
        self.assertEqual(response["contacts"]
                         ["youtube"], profile.contacts.youtube)
