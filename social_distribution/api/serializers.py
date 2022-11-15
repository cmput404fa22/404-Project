from app.models import Author, Post
from rest_framework import serializers
from django.core.paginator import Paginator


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    id = serializers.CharField(source='url')
    host = serializers.CharField()
    displayName = serializers.CharField(source='user.username')
    url = serializers.CharField()
    github = serializers.CharField()
    profileImage = serializers.CharField(source='profile_image_url')

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'displayName',
                  'url', 'github', 'profileImage')


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='post')
    id = serializers.CharField(source='url')
    source = serializers.CharField()
    origin = serializers.CharField()
    description = serializers.CharField()
    contentType = serializers.ChoiceField(
        choices=['text/plain', 'text/markdown', 'application/base64', 'image/png;base64', 'image/jpeg;base64'], source='content_type')
    content = serializers.CharField()
    comments = serializers.CharField(source='comments_url')
    published = serializers.DateTimeField(source='date_published')
    visibility = serializers.ChoiceField(choices=['PUBLIC', 'FRIENDS'])
    unlisted = serializers.BooleanField()
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('type', 'id', 'source', 'origin', 'description', 'contentType',
                  'content', 'comments', 'published', 'visibility', 'unlisted', 'author')
        read_only_fields = ('author',)

    def create(self, validated_data, author):
        return Post(**validated_data, author=author)


def get_paginated_response(items, page, size):
    paginator = Paginator(items, size)
    page_obj = paginator.get_page(page)

    objects = []
    for object in page_obj.object_list:
        objects.append(object.get_json_object())

    res = {"type": objects[0]['type'] + 's', "page": page,
           "size": size, "items": objects}
    return res
