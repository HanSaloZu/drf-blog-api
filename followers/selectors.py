def get_user_followers_ids_list(user):
    followers = user.followers.only("follower_user")
    followers_ids = [i.follower_user.id for i in list(followers)]

    return followers_ids
