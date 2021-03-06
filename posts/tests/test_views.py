import re
from urllib.parse import urlencode

from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.tests import APIViewTestCase, ListAPIViewTestCase

from ..models import Attachment, Like, Post


class RetrieveUpdateDestroyPostAPIViewTestCase(APIViewTestCase):
    def url(self, kwargs):
        return reverse("post", kwargs=kwargs)

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")

        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.user)
        )

        self.first_post = Post.objects.create(author=self.user, body="1")
        Like.objects.create(user=self.user, post=self.first_post)
        Attachment.objects.create(
            post=self.first_post, file_id="1", link="http://localhost:8000/1")
        Attachment.objects.create(
            post=self.first_post, file_id="2", link="http://localhost:8000/2")

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second_user@gmail.com", password="pass")

        self.second_post = Post.objects.create(
            author=self.second_user, body="2")

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url({"id": 1}))

        self.unauthorized_client_error_response_test(response)

    # Retrieve post

    def test_retrieve_post(self):
        # First post
        response = self.client.get(self.url({"id": 1}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.first_post.id)
        self.assertEqual(response.data["body"], self.first_post.body)
        self.assertEqual(response.data["createdAt"],
                         self.first_post.created_at)
        self.assertEqual(response.data["updatedAt"],
                         self.first_post.updated_at)
        self.assertEqual(response.data["likes"], 1)
        self.assertIs(response.data["isLiked"], True)

        self.assertEqual(len(response.data["attachments"]), 2)
        self.assertIn("http://localhost:8000/1", response.data["attachments"])
        self.assertIn("http://localhost:8000/2", response.data["attachments"])

        author = response.data["author"]
        self.assertEqual(len(author), 4)
        self.assertEqual(author["id"], self.user.id)
        self.assertEqual(author["login"], self.user.login)

        # Second post
        response = self.client.get(self.url({"id": 2}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["likes"], 0)
        self.assertIs(response.data["isLiked"], False)
        self.assertEqual(len(response.data["attachments"]), 0)

        author = response.data["author"]
        self.assertEqual(author["id"], self.second_user.id)
        self.assertEqual(author["login"], self.second_user.login)

    def test_retrieve_post_with_invalid_id(self):
        """
        Retrieving a post with an invalid id should return a 404 status code
        """
        response = self.client.get(self.url({"id": 91}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )

    # Destroy post

    def test_delete_post(self):
        """
        Valid post deleting should return a 204 status code
        """
        response = self.client.delete(self.url({"id": 1}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.all().filter(id=1).exists())
        self.assertFalse(Attachment.objects.all().filter(
            post=self.first_post).exists())

    def test_delete_foreign_post(self):
        """
        Deleting foreign post should return a 403 status code
        """
        response = self.client.delete(self.url({"id": 2}))

        self.client_error_response_test(
            response,
            status=self.http_status.HTTP_403_FORBIDDEN,
            code="forbidden",
            messages=["You don't have permission to delete this post"]
        )
        self.assertTrue(Post.objects.all().filter(id=2).exists())

    def test_delete_foreign_post_by_admin_user(self):
        """
        Admin users can delete any posts.
        Valid post deleting should return a 204 status code
        """
        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@user.com", password="admin")
        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(admin)
        )

        response = self.client.delete(self.url({"id": 1}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.all().filter(id=1).exists())

        response = self.client.delete(self.url({"id": 2}))

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.all().filter(id=2).exists())

    def test_delete_post_with_invalid_id(self):
        """
        Deleting a post with an invalid id should return a 404 status code
        """
        response = self.client.delete(self.url({"id": 91}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )

    # Update post

    def test_valid_post_update(self):
        """
        Valid post updating should return a 200 status code
        and an updated post representation
        """
        payload = {
            "body": "New body"
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        post = Post.objects.get(id=1)
        self.assertEqual(payload["body"], response.data["body"])
        self.assertEqual(response.data["body"], post.body)
        self.assertNotEqual(post.updated_at, self.first_post.updated_at)
        self.assertEqual(post.created_at, self.first_post.created_at)

    def test_invalid_post_update(self):
        """
        Invalid post updating should return a 400 status code
        and a list of errors
        """
        payload = {
            "body": None,
            "attachments": True
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.client_error_response_test(
            response,
            messages=[
                "Body field cannot be null",
                "Attachments should be a list of items"
            ],
            fields_errors_dict_len=2
        )

    def test_set_empty_body_for_post(self):
        """
        Post cannot have both fields(body, attachments) empty.
        Post #1 has a list of attachments, so a request
        to set an empty body for a post should return a 200 status code
        """
        payload = {
            "body": ""
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

    def test_set_empty_attachments_for_post(self):
        """
        Post cannot have both fields(body, attachments) empty.
        Post #1 has a body, so a request to set an empty list of attachments
        for post should return a 200 status code
        """
        payload = {
            "attachments": []
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

    def test_set_empty_fields_for_post(self):
        """
        Post cannot have both fields(body, attachments) empty,
        so a request should return a 400 status code
        """
        payload = {
            "body": "",
            "attachments": []
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.client_error_response_test(
            response,
            messages=[
                "One of the two fields (body, attachments) cannot be empty"
            ],
            fields_errors_dict_len=1
        )

    def test_update_foreign_post(self):
        """
        Updating foreign post should return a 403 status code
        """
        payload = {
            "body": "invalid"
        }
        response = self.client.patch(self.url({"id": 2}), payload)

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You don't have permission to edit this post"]
        )

    def test_update_foreign_post_by_admin_user(self):
        """
        Admin users can update any posts.
        Valid post updating should return a 200 status code
        and an updated post representation
        """
        admin = self.UserModel.objects.create_superuser(
            login="Admin", email="admin@gmail.com", password="admin")
        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(admin)
        )

        payload = {
            "body": "New body"
        }
        response = self.client.patch(self.url({"id": 1}), payload)

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        post = Post.objects.get(id=1)
        self.assertEqual(payload["body"], response.data["body"])
        self.assertEqual(response.data["body"], post.body)
        self.assertNotEqual(post.author, admin)

    def test_update_post_with_invalid_id_in_request(self):
        """
        Updating a post with an invalid id should return a 404 status code
        """
        response = self.client.patch(self.url({"id": 91}))

        self.client_error_response_test(
            response,
            code="notFound",
            status=self.http_status.HTTP_404_NOT_FOUND,
            messages=["Invalid id, post is not found"]
        )


class ListCreatePostAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("list_create_post")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        self.user = self.UserModel.objects.create_user(
            login="User", email="user@gmail.com", password="pass")
        self.client.credentials(
            HTTP_AUTHORIZATION=self.generate_jwt_auth_credentials(self.user)
        )

        second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="second_user@gmail.com", password="pass")

        first_post = Post.objects.create(author=self.user, body="First post")
        second_post = Post.objects.create(author=self.user, body="Second post")
        Post.objects.create(author=self.user, body="Last post")

        Like.objects.create(user=self.user, post=second_post)
        Like.objects.create(user=second_user, post=second_post)
        Like.objects.create(user=self.user, post=first_post)

    def test_request_by_unauthenticated_client(self):
        self.client.credentials()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    # Posts list

    def test_posts_list(self):
        """
        A posts list request should return a list of 3 posts
        """
        response = self.client.get(self.url())

        self.check_common_details_of_list_view_response(
            response,
            total_items=3,
            page_size=3
        )

        self.assertEqual(response.data["items"][1]["body"], "Second post")

    def test_posts_list_with_q_parameter(self):
        """
        A posts list request with the q parameter
        should return a list of posts matching the q parameter
        """
        response = self.client.get(self.url({"q": "Last post"}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )

        post = response.data["items"][0]
        self.assertEqual(post["body"], "Last post")

    def test_posts_list_with_limit_parameter(self):
        """
        A request for a list of posts with the limit parameter
        should return a list of posts
        with the number of posts equal to the limit parameter
        """
        response = self.client.get(self.url({"limit": 1}))

        self.check_common_details_of_list_view_response(
            response,
            total_items=3,
            total_pages=3,
            page_size=1
        )

        self.assertEqual(response.data["items"][0]["body"], "Last post")

    def test_posts_list_with_ordering_by_likes(self):
        response = self.client.get(self.url({"ordering": "-likes"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["items"][0]["body"], "Second post")
        self.assertEqual(response.data["items"][0]["likes"], 2)

        self.assertEqual(response.data["items"][1]["body"], "First post")
        self.assertEqual(response.data["items"][1]["likes"], 1)

        self.assertEqual(response.data["items"][2]["body"], "Last post")
        self.assertEqual(response.data["items"][2]["likes"], 0)

        response = self.client.get(self.url({"ordering": "likes"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["items"][0]["body"], "Last post")
        self.assertEqual(response.data["items"][0]["likes"], 0)

        self.assertEqual(response.data["items"][1]["body"], "First post")
        self.assertEqual(response.data["items"][1]["likes"], 1)

        self.assertEqual(response.data["items"][2]["body"], "Second post")
        self.assertEqual(response.data["items"][2]["likes"], 2)

    def test_posts_list_with_ordering_by_creation_date(self):
        response = self.client.get(self.url({"ordering": "-createdAt"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["items"][0]["body"], "Last post")
        self.assertEqual(response.data["items"][1]["body"], "Second post")
        self.assertEqual(response.data["items"][2]["body"], "First post")

        response = self.client.get(self.url({"ordering": "createdAt"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["items"][0]["body"], "First post")
        self.assertEqual(response.data["items"][1]["body"], "Second post")
        self.assertEqual(response.data["items"][2]["body"], "Last post")

    # Create post

    def test_valid_post_creation(self):
        """
        Valid post creation should return a 201 status code
        and a post representation
        """
        payload = {
            "body": "Body"
        }
        response = self.client.post(self.url(), payload)

        self.assertEqual(response.status_code,
                         self.http_status.HTTP_201_CREATED)

        post = Post.objects.get(id=response.data["id"])
        self.assertEqual(response.data["body"], payload["body"])
        self.assertEqual(response.data["body"], post.body)
        self.assertEqual(response.data["createdAt"], post.created_at)
        self.assertEqual(response.data["updatedAt"], post.updated_at)
        self.assertEqual(response.data["likes"], 0)
        self.assertIs(response.data["isLiked"], False)

        self.assertEqual(len(response.data["attachments"]), 0)
        self.assertEqual(response.data["author"]["id"], self.user.id)

    def test_invalid_post_creation(self):
        """
        Invalid post creation should return a 400 status code
        and a list of errors
        """
        payload = {
            "body": get_random_string(length=2001),
            "attachments": False
        }
        response = self.client.post(self.url(), payload)

        self.client_error_response_test(
            response,
            messages=[
                "Body field value is too long",
                "Attachments should be a list of items"
            ],
            fields_errors_dict_len=2
        )

    def test_post_creation_with_empty_fields(self):
        payload = {
            "body": "",
            "attachments": []
        }
        response = self.client.post(self.url(), payload)

        self.client_error_response_test(
            response,
            messages=[
                "One of the two fields (body, attachments) cannot be empty"
            ],
            fields_errors_dict_len=1
        )
