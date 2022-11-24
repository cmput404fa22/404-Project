from ..models import *


class ConnectionInterface():

    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url

    def get_author(author_uuid: str):
        raise NotImplementedError

    def get_all_authors():
        raise NotImplementedError

    def get_followers(author_uuid: str):
        raise NotImplementedError

    def send_follow_request(author_uuid: str):
        raise NotImplementedError

    def get_post(author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def get_all_authors_posts(author_uuid: str):
        raise NotImplementedError

    def send_post(post: Post):
        raise NotImplementedError

    def get_comments(author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def send_comment(comment: Comment):
        raise NotImplementedError

    def get_likes(author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def send_like(like: Like):
        raise NotImplementedError
