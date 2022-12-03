from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

from .models import *
from .utils import url_is_local

import datetime


# Create your tests here.
# run with python manage.py test

class UserModelTest(TestCase):  # base Django User

    def test_create_user(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(username=username, password=password)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))  # hashed

    def test_create_super_user(self):
        username_admin = "admin_user"
        password_admin = "admin_pwd"
        admin = get_user_model().objects.create_superuser(username=username_admin, password=password_admin)
        self.assertEqual(admin.username, username_admin)
        self.assertTrue(admin.check_password(password_admin))  # hashed

    # TODO: TEST FOR UUID BEING GENERATED


class AuthorModelTest(TestCase):  # our Author

    def setUp(self):
        username = "name"
        password = "1234"
        self.host = "localhost"
        self.url = "zombo.com"
        self.github = "github.com"
        self.profile_image_url = "9gag.com"
        user = get_user_model().objects.create_user(username=username, password=password)
        Author.objects.create(user=user,
                              host=self.host,
                              url=self.url,
                              github=self.github,
                              profile_image_url=self.profile_image_url)
        self.author = Author.objects.get(user=user)

    def test_create_author(self):
        self.assertTrue(self.author)  # author created

    def test_author_not_registered(self):
        self.assertFalse(self.author.registered)  # admin has not registered author

    def test_links(self):
        self.assertEqual(self.author.host, self.host)
        self.assertEqual(self.author.url, self.url)
        self.assertEqual(self.author.github, self.github)
        self.assertEqual(self.author.profile_image_url, self.profile_image_url)

    def test_author_get_json(self):
        json_author = self.author.get_json_object()

        self.assertEqual("author", json_author["type"])
        self.assertEqual(self.url, json_author["id"])
        self.assertEqual(self.host, json_author["host"])
        self.assertEqual(self.author.user.username, json_author["displayName"])
        self.assertEqual(self.url, json_author["url"])  # TODO: REDUNDANCY/ERROR IN MODEL? (URL/ID)
        self.assertEqual(self.github, json_author["github"])
        self.assertEqual(self.profile_image_url, json_author["profileImage"])

    # TODO: TEST FOR ON DELETE CASCADE, UUID GENERATION


class RemoteNodeTest(TestCase):  # remote nodes

    def setUp(self):
        username = "remote_node_name"
        password = "remote_node_pwd"
        self.team = 11
        self.remote_base = "remote.com"
        self.remote_home = "remote.com/home"
        remote = get_user_model().objects.create_user(username=username, password=password)
        RemoteNode.objects.create(user=remote,
                                  team=self.team,
                                  base_url=self.remote_base,
                                  home_page=self.remote_home)
        self.remote_node = RemoteNode.objects.get(user=remote)

    def test_create_remote(self):
        self.assertTrue(self.remote_node)  # remote node created

    def test_remote_not_registered(self):
        self.assertFalse(self.remote_node.registered)  # admin has not registered remote node

    def test_links(self):
        self.assertEqual(self.remote_node.base_url, self.remote_base)
        self.assertEqual(self.remote_node.home_page, self.remote_home)

    # TODO: TEST FOR ON DELETE CASCADE, UUID GENERATION


class FollowTest(TestCase):  # following/friending

    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(username=username, password=password)
        Author.objects.create(user=user)
        self.author = Author.objects.get(user=user)

        self.url = "thisiswhothefriendrequestisbeingsentto.com"
        Follow.objects.create(author=self.author, target_url=self.url)
        self.follow = Follow.objects.get(author=self.author)

    def test_create_request(self):
        self.assertTrue(self.follow)

    def test_not_accepted(self):  # not accepted is default
        self.assertFalse(self.follow.accepted)

    def test_link(self):
        self.assertEqual(self.follow.target_url, self.url)

    # TODO: TEST FOR ON DELETE CASCADE, UUID GENERATION


class InboxItemTest(TestCase):

    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(username=username, password=password)
        Author.objects.create(user=user)
        self.author = Author.objects.get(user=user)

        self.type = "POST"
        self.to_url = settings.HOSTNAME + "/authors/" + str(self.author.uuid)
        self.from_url = self.to_url
        InboxItem.objects.create(author=self.author,
                                 type=self.type,
                                 object_url=self.to_url,
                                 from_author_url=self.from_url)
        self.inbox_item = InboxItem.objects.get(author=self.author)

    def test_create_inbox_item(self):
        self.assertTrue(self.inbox_item)

    def test_author_relationship(self):  # author having inbox items etc.
        self.assertEqual(self.inbox_item.author, self.author)
        """
        self.assertEqual(InboxItem.get_posts(author=self.author,
                                             num_of_posts=9001,
                                             page=1),
                         self.inbox_item)
                         """
    # TODO: TEST FOR ON DELETE CASCADE, UUID GENERATION, PROPERLY TESTING THE RELATIONSHIP, TYPE CHOICE INPUT VALIDATION


class PostTest(TestCase):
    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(username=username, password=password)
        Author.objects.create(user=user)
        self.author = Author.objects.get(user=user)

        self.url = "test.com"
        self.title = "Title"
        self.description = "Description"
        self.content_type = "Markdown"
        self.content = "*This is Markdown italics*"
        self.visibility = "PUBLIC"
        Post.objects.create(author=self.author,
                            url=self.url,
                            title=self.title,
                            description=self.description,
                            content_type=self.content_type,
                            content=self.content,
                            visibility=self.visibility)
        self.post = Post.objects.get(author=self.author)  # maybe test getting by other fields too

    def test_create_post(self):
        self.assertTrue(self.post)

    def test_post_fields(self):
        self.assertEqual(self.url, self.post.url)
        self.assertEqual(self.title, self.post.title)
        self.assertEqual(self.description, self.post.description)
        self.assertEqual(self.content_type, self.post.content_type)
        self.assertEqual(self.content, self.post.content)
        self.assertEqual(self.visibility, self.post.visibility)

        self.assertAlmostEqual(timezone.now().timestamp(), self.post.date_published.timestamp(), delta=1)
        # within a second, this will surely never come up as an issue
        self.assertEqual(settings.HOSTNAME, self.post.source)
        self.assertEqual(settings.HOSTNAME, self.post.origin)
        self.assertEqual(0, self.post.comments_count)
        self.assertEqual(0, self.post.likes_count)
        self.assertFalse(self.post.unlisted)
        self.assertFalse(self.post.received)

    def test_post_get_json(self):
        json_post = self.post.get_json_object()

        self.assertEqual(self.url, json_post["id"])
        self.assertEqual(self.title, json_post["title"])
        self.assertEqual(self.description, json_post["description"])
        self.assertEqual(self.content_type, json_post["contentType"])
        self.assertEqual(self.content, json_post["content"])
        self.assertEqual(self.visibility, json_post["visibility"])

        self.assertEqual("post", json_post["type"])
        self.assertAlmostEqual(timezone.now().timestamp(),
                               datetime.datetime.fromisoformat(json_post["published"]).timestamp(), delta=1)
        # within a second, this will surely never come up as an issue
        self.assertEqual(settings.HOSTNAME, json_post["source"])
        self.assertEqual(settings.HOSTNAME, json_post["origin"])
        self.assertEqual(0, json_post["count"])
        self.assertEqual(0, json_post["likes"])
        self.assertFalse(json_post["unlisted"])

        self.assertEqual(self.author.get_json_object(), json_post["author"])

    # TODO: TEST FOR ON DELETE CASCADE, UUID GENERATION, TYPE CHOICE INPUT VALIDATION, OTHER FIELDS

# TODO: COMMENT AND LIKE TESTING

# TODO: SUBCLASS TEST CASE WITH COMMON SETUP TO NOT REDO CREATING USERS EACH TIME (SAME WITH TEARDOWN?)
#  OR JUST MAKE A GLOBAL FUNCTION
