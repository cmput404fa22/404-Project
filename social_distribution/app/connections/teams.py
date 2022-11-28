from ..models import *
import requests
from .base import ConnectionInterface
import os


class Team14Connection(ConnectionInterface):
    pass


class Team8Connection(ConnectionInterface):

    def get_author(self, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/"
        response = requests.request("GET", url)

        if (response.status_code != 200):
            return None

        author_json = response.json()
        author_json["url"] = author_json["url"][:-1]
        author_object = {"type": "author", "id": author_json["url"],
                         "host": author_json["host"], "displayName": author_json["displayName"],
                         "url": author_json["url"], "github": author_json["github"],
                         "profileImage": "?"}

        return author_object

    def get_all_authors(self):
        url = self.base_url + "authors"
        response = requests.request("GET", url)

        if (response.status_code != 200):
            print(response.text)
            return []

        response_json = response.json()
        if (response_json.get('items') is None or len(response_json.get('items')) == 0):
            print(response.text)
            return []

        author_objects = []
        for author_json in response_json['items']:
            author_json["url"] = author_json["url"][:-1]
            obj = {"type": "author", "id": author_json["url"],
                   "host": author_json["host"], "displayName": author_json["displayName"],
                   "url": author_json["url"], "github": author_json["github"],
                   "profileImage": ""}
            author_objects.append(obj)

        return author_objects

    def get_all_authors_posts(self, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/posts"
        response = requests.request("GET", url)

        if (response.status_code != 200):
            print(response.text)
            return []

        response_json = response.json()
        if (response_json.get('items') is None or len(response_json.get('items')) == 0):
            print(response.text)
            return []

        posts_objects = []
        for posts_json in response_json['items']:
            author_json = posts_json["author"]
            author_json["url"] = author_json["url"][:-1]
            author_object = {"type": "author", "id": author_json["url"],
                             "host": author_json["host"], "displayName": author_json["displayName"],
                             "url": author_json["url"], "github": author_json["github"],
                             "profileImage": ""}
            post_object = {"type": "post", "title": posts_json["title"], "id": posts_json["id"], "source": posts_json["source"],
                           "origin": posts_json["origin"], "description": "", "contentType": posts_json["contentType"], "content": posts_json["content"],
                           "author": author_object, "count": posts_json["count"], "comments": posts_json["comments"], "likes": 0,
                           "published": posts_json["published"], "visibility": posts_json["visibility"], "unlisted": posts_json["unlisted"]}
            posts_objects.append(post_object)

        return posts_objects


class RemoteNodeConnection():
    teams = {
        "https://c404-team8.herokuapp.com/api/": {"num": 8, "conn": Team8Connection},
        "https://social-distribution-14degrees2.herokuapp.com/api/": {"num": 15, "conn": Team14Connection}
    }

    def __init__(self, url: str):
        base_url = url.split("authors")[0]
        username = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_USERNAME")
        password = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_PASSWORD")
        self.conn = self.teams[base_url]["conn"](username, password, base_url)
