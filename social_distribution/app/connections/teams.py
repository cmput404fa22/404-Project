from ..models import *
import requests
from .base import ConnectionInterface
import os
import json


class Team15Connection(ConnectionInterface):
    def get_author(self, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/"
        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            return None

        author_json = response.json()["items"]
        author_object = {"id": author_json["id"],
                         "displayName": author_json["displayName"],
                         "url": author_json["url"], "github": author_json["github"],
                         "profileImage": author_json["profileImage"]}

        return author_object

    def get_all_authors(self):
        url = self.base_url + "authors"
        response = requests.request(
            "GET", url, auth=(self.username, self.password))
        if (response.status_code != 200):
            print(response.text)
            return []
        response_json = response.json()
        if (response_json is None or len(response_json) == 0):
            print(response.text)
            return []
        author_objects = []
        for author_json in response_json['items']:
            obj = {"id": author_json["id"],
                   "displayName": author_json["displayName"],
                   "url": author_json["url"], "github": author_json["github"],
                   "profileImage": author_json["profileImage"]}
            author_objects.append(obj)

        return author_objects


class Team14Connection(ConnectionInterface):

    def get_post(self, author_uuid: str, post_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/posts/{post_uuid}"

        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            return None

        posts_json = response.json()
        author_json = posts_json["author"]
        author_json["url"] = author_json["url"][:-1]
        author_object = {"id": author_json["url"],
                         "displayName": author_json["display_name"],
                         "url": author_json["url"], "github": author_json["github_handle"],
                         "profileImage": author_json["profile_image"]}
        post_object = {"title": posts_json["title"], "id": posts_json["id"], "source": posts_json["source"],
                       "origin": posts_json["origin"], "description": "", "contentType": posts_json["content_type"], "content": posts_json["content"],
                       "author": author_object, "likesCount": posts_json["likes_count"],
                       "createdAt": posts_json["created_at"], "visibility": posts_json["visibility"], "unlisted": posts_json["unlisted"], "editedAt": posts_json["edited_at"]}

        return post_object

    #     def send_post(self, post: Post, author_uuid: str):
    #         url = self.base_url + f"authors/{author_uuid}/inbox/"
    #         post_uuid = post.uuid
    #         posts_author_uuid = post.author.uuid

    #         body = {
    #             "type": "post",
    #             "post": {
    #                 "id": post_uuid,
    #                 "author": {
    #                     "id": posts_author_uuid,
    #                     "url": post.url,
    #                 }
    #             }
    #         }
    #         print(url)
    #         print(json.dumps(body))
    #         raise Exception("stop here")
    #         # response = requests.request("POST", url, json=body)
    #         # if (response.status_code != 201):
    #         #     print(response.status_code)
    #         #     print(response.text)
    #         #     return None
    #         # return body

    def send_follow_request(self, sender: Author, author_uuid):
        url = self.base_url + f"authors/{author_uuid}/inbox/"

        followed = self.get_author(author_uuid)
        sender = sender.get_json_object()

        body = {
            "type": "follow",
            "sender": {
                "url": sender['id'],
                "id": sender['id'].split("/")[-1]
            },
            "receiver": {
                "url": followed["id"],
                "id": followed['id'].split("/")[-1]
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", url, headers=headers, json=body, auth=(self.username, self.password))

        if (response.status_code != 201):
            print(response.status_code)
            print(response.text)
            return None

        return followed

    def get_author(self, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/"
        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            return None

        author_json = response.json()
        author_json["url"] = author_json["url"][:-1]
        author_object = {"id": author_json["url"],
                         "displayName": author_json["display_name"],
                         "url": author_json["url"], "github": author_json["github_handle"],
                         "profileImage": author_json["profile_image"]}

        return author_object

    def get_all_authors(self):
        url = self.base_url + "authors"
        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            print(response.text)
            return []

        response_json = response.json()
        if (response_json is None or len(response_json) == 0):
            print(response.text)
            return []

        author_objects = []
        for author_json in response_json:
            author_json["url"] = author_json["url"][:-1]
            obj = {"id": author_json["url"],
                   "displayName": author_json["display_name"],
                   "url": author_json["url"], "github": author_json["github_handle"],
                   "profileImage": author_json["profile_image"]}
            author_objects.append(obj)

        return author_objects

    def get_all_authors_posts(self, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/posts"
        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            print(response.text)
            return []

        response_json = response.json()
        if (response_json is None or len(response_json) == 0):
            print(response.text)
            return []

        posts_objects = []
        for posts_json in response_json:
            author_json = posts_json["author"]
            author_json["url"] = author_json["url"][:-1]
            author_object = {"id": author_json["url"],
                             "displayName": author_json["display_name"],
                             "url": author_json["url"], "github": author_json["github_handle"],
                             "profileImage": author_json["profile_image"]}
            post_object = {"title": posts_json["title"], "id": posts_json["id"], "source": posts_json["source"],
                           "origin": posts_json["origin"], "description": "", "contentType": posts_json["content_type"], "content": posts_json["content"],
                           "author": author_object, "likesCount": posts_json["likes_count"],
                           "createdAt": posts_json["created_at"], "visibility": posts_json["visibility"], "unlisted": posts_json["unlisted"], "editedAt": posts_json["edited_at"]}
            posts_objects.append(post_object)

        return posts_objects


class Team8Connection(ConnectionInterface):

    def send_post(self, post: Post, author_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/inbox/"
        body = post.get_json_object()
        response = requests.request("POST", url, json=body)
        if (response.status_code != 201):
            print(response.status_code)
            print(response.text)
            return None
        return body

    def send_follow_request(self, sender: Author, author_uuid):
        url = self.base_url + f"authors/{author_uuid}/inbox/"

        followed = self.get_author(author_uuid)
        sender = sender.get_json_object()
        body = {
            "type": "follow",
            "summary": f"{sender['displayName']} wants to follow {followed['displayName']}",
            "actor": {
                "type": "author",
                "id": sender['id'],
                "url": sender['url'],
                "host": sender['host'],
                "displayName": sender['displayName'],
                "github": sender['github'],
                "profileImage": sender['profileImage']
            },
            "object": {
                "type": "author",
                "id": followed["id"],
                "host": followed["host"],
                "displayName": followed["displayName"],
                "url":  followed["url"],
                "github": followed["github"],
                "profileImage": followed["profileImage"]
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, json=body)
        if (response.status_code != 201 or response.status_code != 200):
            print(response.status_code)
            print(response.text)
            return None

        return followed

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

    def get_post(self, author_uuid: str, post_uuid: str):
        url = self.base_url + f"authors/{author_uuid}/posts/{post_uuid}"

        response = requests.request(
            "GET", url, auth=(self.username, self.password))

        if (response.status_code != 200):
            return None

        posts_json = response.json()
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

        return post_object


class RemoteNodeConnection():
    teams = {
        "https://c404-team8.herokuapp.com/api/": {"num": 8, "conn": Team8Connection},
        "https://social-distribution-14degrees.herokuapp.com/api/": {"num": 14, "conn": Team14Connection},
        "https://fallsocialuahank.herokuapp.com/service/": {"num": 15, "conn": Team15Connection}
    }

    def __init__(self, url: str):
        base_url = url.split("authors")[0]
        self.username = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_USERNAME")
        self.password = os.environ.get(
            "TEAM_" + str(self.teams[base_url]["num"]) + "_PASSWORD")
        self.conn = self.teams[base_url]["conn"](
            self.username, self.password, base_url)
