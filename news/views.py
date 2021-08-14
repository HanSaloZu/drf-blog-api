from utils.views import LoginRequiredAPIView
from posts.mixins import ListPostsAPIViewMixin
from followers.selectors import get_user_followings_ids_list


class NewsAPIView(LoginRequiredAPIView, ListPostsAPIViewMixin):
    """
    Lists posts created by users that the authenticated user follows
    """

    def get_queryset(self):
        posts = super().get_queryset()
        return posts.filter(
            author_id__in=get_user_followings_ids_list(self.request.user))
