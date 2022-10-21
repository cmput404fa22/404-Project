from email.policy import default
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # extend user model

    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    host = models.CharField(max_length=64)
    display_name = models.CharField(max_length=32)
    url = models.CharField(max_length=200)
    github = models.CharField(max_length=64)
    profile_image_url = models.CharField(max_length=200)


class Follower(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    follower_url = models.CharField(max_length=200)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # author has followers


class InboxItem(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = (
        ('POST', 'post'),
        ('COMMENT', 'comment'),
        ('LIKE', 'like'),
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    object_url = models.CharField(max_length=200)  # remote or local

    author = models.ForeignKey(Author)  # author has InboxItems


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    url = models.CharField(max_length=200)
    title = models.CharField(max_length=64)
    date_published = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=64)
    origin = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    content_type = models.CharField(max_length=64)
    categories = models.CharField(max_length=64)
    comments_count = models.CharField(max_length=64)
    comments_url = models.CharField(max_length=64)
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'public'),
        ('PRIVATE', 'private'),
    )
    visibility = models.CharField(max_length=1, choices=VISIBILITY_CHOICES)
    unlisted = models.BooleanField(default=False)
    author_url = models.CharField(max_length=200)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # posts have authors


class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    commenter_url = models.CharField(max_length=200)
    comment = models.CharField(max_length=64)
    content_type = models.CharField(max_length=64)
    date_published = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post)  # posts have comments


class Like(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    liker_url = models.CharField(max_length=200)

    post = models.ForeignKey(Post)  # posts have likes
    comment = models.ForeignKey(Comment)  # comments have likes
