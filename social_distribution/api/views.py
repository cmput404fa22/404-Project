from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from app.models import Author, Post, Follow
from .serializers import get_paginated_response


@api_view(["GET"])
def get_author(request, author_id):
    author = get_object_or_404(Author, uuid=author_id)
    return Response(author.get_json_object())


@api_view(["GET"])
def get_authors(request):
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '10'))
    authors = Author.objects.all()
    response = get_paginated_response(authors, page, size)
    return Response(response)


@api_view(["GET"])
def get_followers(request, author_id):
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '10'))
    followers = Follow.objects.get(
        author=Author.objects.get(uuid=author_id).user)
    response = get_paginated_response(followers, page, size)
    return Response(response)


@api_view(["GET"])
def get_post(request, author_id, post_id):
    post = get_object_or_404(Post, uuid=post_id)
    if post.visibility != 'PUBLIC':
        return Response({'error': 'Unauthorized'}, status=403)
    return Response(post.get_json_object())


@api_view(["GET"])
def get_posts(request, author_id):
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '10'))
    posts = Post.objects.filter(
        visibility='PUBLIC', author=Author.objects.get(uuid=author_id).user)
    response = get_paginated_response(posts, page, size)
    return Response(response)


@api_view(["POST"])
def post_to_inbox(request, author_id):
    return Response(response)
