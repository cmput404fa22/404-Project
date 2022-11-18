from distutils.command.upload import upload
from email.policy import default
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # extend user model

    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    host = models.TextField(default="http://" + settings.HOSTNAME)
    url = models.TextField()
    github = models.TextField(blank=True)

    profile_image_url = models.TextField(
        default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png')
    registered = models.BooleanField(default=False)

    def get_json_object(self):
        author_object = {"type": "author", "id": self.url,
                         "host": self.host, "displayName": self.user.username,
                         "url": self.url, "github": self.github,
                         "profileImage": self.profile_image_url}
        return author_object


class Follow(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    target_url = models.TextField()
    accepted = models.BooleanField(default=False)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # author has followers


class InboxItem(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = (
        ('POST', 'post'),
        ('COMMENT', 'comment'),
        ('LIKE', 'like'),
        ('FOLLOW', 'follow'),
    )
    type = models.CharField(max_length=13, choices=TYPE_CHOICES)
    # url to the object InboxItem is referring to, ie the post, comment, like
    object_url = models.TextField(null=True)
    # url to the author that caused this InboxItem
    from_author_url = models.TextField()
    # username of the author that caused this InboxItem
    from_username = models.TextField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)  # author has InboxItems

    def get_posts(author, num_of_posts, page):
        posts = InboxItem.objects.filter(author=author, type="POST")
        paginator = Paginator(posts, num_of_posts)
        page = paginator.page(page)

        post_objects = []
        for item in page:
            if item.object_url.startswith("http://" + settings.HOSTNAME):
                post = Post.objects.get(item.object_url.split["/"][-1])
                post_objects.append(post)
            else:
                # TODO: query remote node for post
                continue

        return paginator


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    url = models.TextField()
    title = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    source = models.TextField(default="http://" + settings.HOSTNAME)
    origin = models.TextField(default="http://" + settings.HOSTNAME)
    description = models.TextField()
    content_type = models.TextField()
    content = models.TextField()
    categories = models.TextField()
    comments_count = models.IntegerField(default=0)
    comments_url = models.TextField()
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'public'),
        ('PRIVATE', 'private'),
    )
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)
    author_url = models.TextField()

    received = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # posts have authors

    def get_json_object(self):
        post_object = {"type": "post", "id": self.url, "source": self.source,
                       "origin": self.origin, "description": self.description, "contentType": self.content_type, "content": self.content,
                       "author": self.author.author.get_json_object(), "count": self.comments_count, "comments": self.comments_url,
                       "published": self.date_published.isoformat(), "visibility": self.visibility, "unlisted": self.unlisted}
        return post_object


class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    commenter_url = models.TextField()
    comment = models.TextField()
    content_type = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)  # posts have comments


class Like(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    liker_url = models.TextField()

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)  # posts have likes
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE)  # comments have likes
