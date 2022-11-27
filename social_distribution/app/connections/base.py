from ..models import *


class ConnectionInterface():

    def __init__(self, username, password, base_url):
        self.username = username
        self.password = password
        self.base_url = base_url

    def get_author(self, author_uuid: str):
        raise NotImplementedError

    def get_all_authors(self, ):
        raise NotImplementedError

    def get_followers(self, author_uuid: str):
        raise NotImplementedError

    def send_follow_request(self, author_uuid: str):
        raise NotImplementedError

    def get_post(self, author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def get_all_authors_posts(self, author_uuid: str):
        raise NotImplementedError

    def send_post(self, post: Post, author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def get_comments(self, author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def send_comment(self, comment: Comment, author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def get_likes(self, author_uuid: str, post_uuid: str):
        raise NotImplementedError

    def send_like(self, like: Like, author_uuid: str, post_uuid: str):
        raise NotImplementedError
