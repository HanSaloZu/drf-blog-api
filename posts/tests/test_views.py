from django.urls import reverse

from utils.tests import APIViewTestCase

from ..models import Post, Attachment, Like


class RetrieveUpdateDestroyPostAPIViewTestCase(APIViewTestCase):
    def url(self, kwargs):
        return reverse("post", kwargs=kwargs)

    def setUp(self):
        credentials = {"email": "user@gmail.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="User", **credentials)
        self.client.login(**credentials)

        self.first_post = Post.objects.create(
            author=self.user, title="First post", body="Body")
        Like.objects.create(user=self.user, post=self.first_post)
        Attachment.objects.create(
            post=self.first_post, file_id="1", link="http://localhost:8000/1")
        Attachment.objects.create(
            post=self.first_post, file_id="2", link="http://localhost:8000/2")

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="seconds_user@gmail.com", password="pass")

        self.second_post = Post.objects.create(
            author=self.second_user, title="Second post", body="")

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url({"id": 1}))

        self.unauthorized_client_error_response_test(response)

    # Retrieve post

    def test_retrieve_post(self):
        # First post
        response = self.client.get(self.url({"id": 1}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        self.assertEqual(response.data["id"], self.first_post.id)
        self.assertEqual(response.data["title"], self.first_post.title)
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
        Valid post deleting should return a 200 status code
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
        response = self.client.patch(
            self.url({"id": 1}), payload, content_type="application/json")

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)

        post = Post.objects.get(id=1)
        self.assertEqual(payload["body"], response.data["body"])
        self.assertEqual(response.data["title"], post.title)
        self.assertEqual(response.data["body"], post.body)
        self.assertNotEqual(post.updated_at, self.first_post.updated_at)
        self.assertEqual(post.created_at, self.first_post.created_at)

    def test_invalid_post_update(self):
        """
        Incalid post updating should return a 400 status code
        and a list of errors
        """
        payload = {
            "title": "",
            "body": None,
            "attachments": True
        }
        response = self.client.patch(
            self.url({"id": 1}), payload, content_type="application/json")

        self.client_error_response_test(
            response,
            messages=[
                "Title field cannot be empty",
                "Body field cannot be null",
                "Attachments should be a list of items"
            ],
            fields_errors_dict_len=3
        )

    def test_update_foreign_post(self):
        """
        Updating foreign post should return a 403 status code
        """
        payload = {
            "title": "2nd post"
        }
        response = self.client.patch(self.url({"id": 2}), payload)

        self.client_error_response_test(
            response,
            code="forbidden",
            status=self.http_status.HTTP_403_FORBIDDEN,
            messages=["You don't have permission to edit this post"]
        )

    def test_update_post_with_invalid_id(self):
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
