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
    host = models.TextField()
    display_name = models.TextField()
    url = models.TextField()
    github = models.TextField()
    profile_image_url = models.TextField()


class Follower(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    follower_url = models.TextField()

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
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)  # CharField seems good for this one
    object_url = models.TextField()  # remote or local

    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # author has InboxItems


class Post(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    url = models.TextField()
    title = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)
    source = models.TextField()
    origin = models.TextField()
    description = models.TextField()
    content_type = models.TextField()
    categories = models.TextField()
    comments_count = models.TextField()
    comments_url = models.TextField()
    VISIBILITY_CHOICES = (
        ('PUBLIC', 'public'),
        ('PRIVATE', 'private'),
    )
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES)  # again probably good CharField
    unlisted = models.BooleanField(default=False)
    author_url = models.TextField()

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)  # posts have authors


class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    commenter_url = models.TextField()
    comment = models.TextField()
    content_type = models.TextField()
    date_published = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # posts have comments


class Like(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    liker_url = models.TextField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # posts have likes
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  # comments have likes
