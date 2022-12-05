from distutils.command.upload import upload
from email.policy import default
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # extend user model

    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    host = models.TextField(default=settings.HOSTNAME)
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


class RemoteNode(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # extend user model
    uuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False)
    base_url = models.TextField(unique=True)
    home_page = models.TextField(unique=True, default="#")
    team = models.IntegerField(unique=True)
    registered = models.BooleanField(default=False)


class Follow(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    target_url = models.TextField()
    accepted = models.BooleanField(default=False)

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)  # author has followers


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    url = models.TextField()
    title = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    source = models.TextField(default=settings.HOSTNAME)
    origin = models.TextField(default=settings.HOSTNAME)
    description = models.TextField()
    content_type = models.TextField()
    content = models.TextField()
    categories = models.TextField()
    comments_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    comments_url = models.TextField()
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'public'),
        ('FRIENDS', 'friends'),
    )
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)
    author_url = models.TextField()

    received = models.BooleanField(default=False)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)  # posts have authors

    def get_json_object(self):
        post_object = {"type": "post", "title": self.title, "id": self.url, "uuid": self.uuid, "source": self.source,
                       "origin": self.origin, "description": self.description, "contentType": self.content_type, "content": self.content,
                       "author": self.author.get_json_object(), "count": self.comments_count, "comments": self.comments_url, "likes": self.likes_count,
                       "published": self.date_published.isoformat(), "visibility": self.visibility, "unlisted": self.unlisted}
        return post_object


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
    date_published = models.DateTimeField(default=timezone.now, null=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)  # author has InboxItems
    friends_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True)  # author has InboxItems


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
        Post, on_delete=models.CASCADE, null=True)  # posts have likes
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True)  # comments have likes
