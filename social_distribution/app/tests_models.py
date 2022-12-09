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
        user = get_user_model().objects.create_user(
            username=username, password=password)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))  # hashed

    def test_create_super_user(self):
        username_admin = "admin_user"
        password_admin = "admin_pwd"
        admin = get_user_model().objects.create_superuser(
            username=username_admin, password=password_admin)
        self.assertEqual(admin.username, username_admin)
        self.assertTrue(admin.check_password(password_admin))  # hashed


class AuthorModelTest(TestCase):  # our Author

    def setUp(self):
        username = "name"
        password = "1234"
        self.host = "localhost"
        self.url = "zombo.com"
        self.github = "github.com"
        self.profile_image_url = "9gag.com"
        self.user = get_user_model().objects.create_user(
            username=username, password=password)
        Author.objects.create(user=self.user,
                              host=self.host,
                              url=self.url,
                              github=self.github,
                              profile_image_url=self.profile_image_url)
        self.author = Author.objects.get(user=self.user)

    def test_create_author(self):
        self.assertTrue(self.author)  # author created

    def test_author_not_registered(self):
        # admin has not registered author
        self.assertFalse(self.author.registered)

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
        # REDUNDANCY IN MODEL? (URL/ID ARE IDENTICAL)
        self.assertEqual(self.url, json_author["url"])
        self.assertEqual(self.github, json_author["github"])
        self.assertEqual(self.profile_image_url, json_author["profileImage"])

    def test_author_delete(self):
        self.author.delete()
        self.assertRaisesRegex(Exception, "Author matching query does not exist.", Author.objects.get, user=self.user)

    def test_author_delete_cascade(self):  # setUp runs before each test, author restored each time
        self.user.delete()
        self.assertRaisesRegex(Exception, "Author matching query does not exist.", Author.objects.get, host=self.host)


class RemoteNodeTest(TestCase):  # remote nodes

    def setUp(self):
        username = "remote_node_name"
        password = "remote_node_pwd"
        self.team = 11
        self.remote_base = "remote.com"
        self.remote_home = "remote.com/home"
        self.remote = get_user_model().objects.create_user(
            username=username, password=password)
        RemoteNode.objects.create(user=self.remote,
                                  team=self.team,
                                  base_url=self.remote_base,
                                  home_page=self.remote_home)
        self.remote_node = RemoteNode.objects.get(user=self.remote)

    def test_create_remote(self):
        self.assertTrue(self.remote_node)  # remote node created

    def test_remote_not_registered(self):
        # admin has not registered remote node
        self.assertFalse(self.remote_node.registered)

    def test_links(self):
        self.assertEqual(self.remote_node.base_url, self.remote_base)
        self.assertEqual(self.remote_node.home_page, self.remote_home)

    def test_remote_node_delete(self):
        self.remote_node.delete()
        self.assertRaisesRegex(Exception, "RemoteNode matching query does not exist.", RemoteNode.objects.get,
                               user=self.remote)

    def test_remote_node_delete_cascade(self):  # setUp runs before each test, remote node restored each time
        self.remote.delete()
        self.assertRaisesRegex(Exception, "RemoteNode matching query does not exist.", RemoteNode.objects.get,
                               team=self.team)


class FollowTest(TestCase):  # following/friending

    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(
            username=username, password=password)
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

    def test_follow_delete(self):
        self.follow.delete()
        self.assertRaisesRegex(Exception, "Follow matching query does not exist.", Follow.objects.get,
                               author=self.author)

    def test_follow_delete_cascade(self):  # setUp runs before each test, follow restored each time
        self.author.delete()
        self.assertRaisesRegex(Exception, "Follow matching query does not exist.", Follow.objects.get,
                               target_url=self.url)


class InboxItemTest(TestCase):

    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(
            username=username, password=password)
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

    def test_inbox_item_delete(self):
        self.inbox_item.delete()
        self.assertRaisesRegex(Exception, "InboxItem matching query does not exist.", InboxItem.objects.get,
                               author=self.author)

    def test_inbox_item_delete_cascade(self):  # setUp runs before each test, inbox item restored each time
        self.author.delete()
        self.assertRaisesRegex(Exception, "InboxItem matching query does not exist.", InboxItem.objects.get,
                               object_url=self.to_url)


class PostTest(TestCase):
    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(
            username=username, password=password)
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
        self.post = Post.objects.get(author=self.author)

    def test_create_post(self):
        self.assertTrue(self.post)

    def test_post_fields(self):
        self.assertEqual(self.url, self.post.url)
        self.assertEqual(self.title, self.post.title)
        self.assertEqual(self.description, self.post.description)
        self.assertEqual(self.content_type, self.post.content_type)
        self.assertEqual(self.content, self.post.content)
        self.assertEqual(self.visibility, self.post.visibility)

        self.assertAlmostEqual(timezone.now().timestamp(
        ), self.post.date_published.timestamp(), delta=1)
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

    def test_post_delete(self):
        self.post.delete()
        self.assertRaisesRegex(Exception, "Post matching query does not exist.", Post.objects.get,
                               author=self.author)

    def test_post_delete_cascade(self):  # setUp runs before each test, post restored each time
        self.author.delete()
        self.assertRaisesRegex(Exception, "Post matching query does not exist.", Post.objects.get,
                               content=self.content)


class CommentTest(TestCase):
    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(
            username=username, password=password)
        self.author_url = "zombo.com"
        Author.objects.create(user=user, url=self.author_url)
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
        self.post = Post.objects.get(author=self.author)

        self.comment = "This is a comment"
        Comment.objects.create(commenter_url=self.author_url,
                               comment=self.comment,
                               content_type=self.content_type,
                               post=self.post)
        self.comment_object = Comment.objects.get(comment=self.comment)

    def test_create_comment(self):
        self.assertTrue(self.post)

    def test_comment_fields(self):
        self.assertEqual(self.comment_object.commenter_url, self.author_url)
        self.assertEqual(self.comment_object.comment, self.comment)
        self.assertEqual(self.comment_object.content_type, self.content_type)
        self.assertAlmostEqual(timezone.now().timestamp(
        ), self.comment_object.date_published.timestamp(), delta=1)
        # within a second, this will surely never come up as an issue

    def test_comment_relationship(self):
        self.assertEqual(self.comment_object.commenter_url, self.author.url)

    def test_comment_delete(self):
        self.comment_object.delete()
        self.assertRaisesRegex(Exception, "Comment matching query does not exist.", Comment.objects.get,
                               comment=self.comment)

    def test_comment_delete_cascade(self):  # setUp runs before each test, comment restored each time
        self.post.delete()
        self.assertRaisesRegex(Exception, "Comment matching query does not exist.", Comment.objects.get,
                               post=self.post)


class LikeTest(TestCase):
    def setUp(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(
            username=username, password=password)
        self.liker_url = "zombo.com"
        Author.objects.create(user=user, url=self.liker_url)
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
        self.post = Post.objects.get(author=self.author)

        self.comment = "This is a comment"
        Comment.objects.create(commenter_url=self.liker_url,
                               comment=self.comment,
                               content_type=self.content_type,
                               post=self.post)
        self.comment_object = Comment.objects.get(comment=self.comment)

        Like.objects.create(liker_url=self.liker_url, post=self.post)
        Like.objects.create(liker_url=self.liker_url, comment=self.comment_object)
        self.like_post = Like.objects.get(post=self.post)
        self.like_comment = Like.objects.get(comment=self.comment_object)

    def test_create_like(self):
        self.assertTrue(self.like_post)
        self.assertTrue(self.like_comment)

    def test_like_fields(self):
        self.assertEqual(self.like_post.liker_url, self.liker_url)

    def test_like_relationship(self):
        self.assertEqual(self.like_post.liker_url, self.author.url)
        self.assertEqual(self.like_comment.liker_url, self.author.url)

    def test_like_delete(self):
        self.like_post.delete()
        self.assertRaisesRegex(Exception, "Like matching query does not exist.", Like.objects.get,
                               post=self.post)
        self.like_comment.delete()
        self.assertRaisesRegex(Exception, "Like matching query does not exist.", Like.objects.get,
                               comment=self.comment_object)

    def test_like_delete_cascade(self):  # setUp runs before each test, likes restored each time
        self.post.delete()
        self.assertRaisesRegex(Exception, "Like matching query does not exist.", Like.objects.get,
                               post=self.post)
        self.comment_object.delete()
        self.assertRaisesRegex(Exception, "Like matching query does not exist.", Like.objects.get,
                               comment=self.comment_object)
