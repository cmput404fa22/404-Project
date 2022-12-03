from app.models import Author, Post
from rest_framework import serializers
from django.core.paginator import Paginator


class StringListField(serializers.ListField):
    child = serializers.CharField()


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    id = serializers.CharField(source='url')
    host = serializers.CharField()
    displayName = serializers.CharField(source='user.username')
    url = serializers.CharField()
    github = serializers.CharField(allow_blank=True)
    profileImage = serializers.CharField(source='profile_image_url')

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName',
                  'url', 'github', 'profileImage')


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='post')
    id = serializers.CharField(source='url')
    source = serializers.CharField()
    title = serializers.CharField()
    origin = serializers.CharField()
    description = serializers.CharField()
    contentType = serializers.ChoiceField(
        choices=['text/plain', 'text/markdown', 'application/base64', 'image/png;base64', 'image/jpeg;base64'], source='content_type')
    content = serializers.CharField()
    comments = serializers.CharField(source='comments_url')
    published = serializers.DateTimeField(source='date_published')
    visibility = serializers.ChoiceField(choices=['PUBLIC', 'FRIENDS'])
    categories = StringListField()
    unlisted = serializers.BooleanField()
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('type', 'id', 'source', 'title', 'origin', 'description', 'contentType',
                  'content', 'comments', 'published', 'visibility', 'unlisted', 'author', 'categories')
        read_only_fields = ('author',)

    def create(self, validated_data, author):
        return Post(**validated_data, author=author)
