from django.urls import reverse
from urllib.parse import urlencode

from utils.tests import ListAPIViewTestCase
from posts.models import Post
from followers.services import follow, unfollow


class NewsAPIViewTestCase(ListAPIViewTestCase):
    def url(self, parameters={}):
        url = reverse("news")
        if parameters:
            url += "?" + urlencode(parameters)

        return url

    def setUp(self):
        credentials = {"email": "user@gmail.com", "password": "pass"}
        self.user = self.UserModel.objects.create_user(
            login="User", **credentials)
        self.client.login(**credentials)

        self.second_user = self.UserModel.objects.create_user(
            login="SecondUser", email="seconduser@gmail.com", password="pass")
        third_user = self.UserModel.objects.create_user(
            login="ThirdUser", email="thirduser@gmail.com", password="pass")
        follow(self.user, self.second_user)

        Post.objects.create(author=self.user, title="post #1 by user")
        self.first_news_post = Post.objects.create(
            author=self.second_user, title="post #1 by second user")
        self.second_news_post = Post.objects.create(
            author=self.second_user, title="post #2 by second user")
        Post.objects.create(author=third_user, title="post #1 by third user")

    def test_request_by_unauthenticated_client(self):
        self.client.logout()
        response = self.client.get(self.url())

        self.unauthorized_client_error_response_test(response)

    def test_news(self):
        """
        A news list request should return posts
        created by users that the authenticated user follows
        """
        response = self.client.get(self.url())

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=2
        )

        self.assertEqual(response.data["items"]
                         [0]["id"], self.second_news_post.id)
        self.assertEqual(response.data["items"]
                         [1]["id"], self.first_news_post.id)

    def test_news_with_limit_parameter(self):
        """
        A news list request with the limit parameter
        should return a list of posts
        created by users that the authenticated user follows
        with the number of posts equal to the limit parameter
        """
        response = self.client.get(self.url({"limit": "1"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.check_common_details_of_list_view_response(
            response,
            total_items=2,
            page_size=1,
            total_pages=2
        )

        self.assertEqual(response.data["items"]
                         [0]["id"], self.second_news_post.id)

    def test_news_with_q_parameter(self):
        """
        A news list request with the q parameter
        should return a list of posts that match the q parameter
        and created by users that the authenticated user follows
        """
        response = self.client.get(self.url({"q": "#1"}))

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.check_common_details_of_list_view_response(
            response,
            total_items=1,
            page_size=1
        )

        self.assertEqual(response.data["items"]
                         [0]["id"], self.first_news_post.id)

    def test_news_without_followings(self):
        """
        If the user has no followings, news should be empty
        """
        unfollow(self.user, self.second_user)
        response = self.client.get(self.url())

        self.assertEqual(response.status_code, self.http_status.HTTP_200_OK)
        self.check_common_details_of_list_view_response(response)
