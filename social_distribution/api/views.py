from .serializers import AuthorSerializer, PostSerializer
from app.models import Author, Post, Follow
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


class AuthorItems(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': AuthorSerializer})
    def get(self, request):
        authors = Author.objects.all()

        results = self.paginate_queryset(authors, request, view=self)
        serializer = AuthorSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class SingleAuthor(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': AuthorSerializer})
    def get(self, request, uuid):
        author = Author.objects.get(uuid=uuid)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)


class PostItems(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': PostSerializer})
    def get(self, request, author_id):
        posts = Post.objects.filter(uuid=author_id)

        results = self.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class SinglePost(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': PostSerializer})
    def get(self, request, author_id, post_id):
        post = Post.objects.get(uuid=post_id)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)


# def authors_list(request):
#     """

#     """
#     if request.method == 'GET':
#         authors = Author.objects.all()
#         serializer = AuthorSerializer(authors, many=True)
#         return JsonResponse(serializer.data, safe=False)

# @api_view(["GET"])
# def get_author(request, author_id):
#     author = get_object_or_404(Author, uuid=author_id)
#     return Response(author.get_json_object())


# @api_view(["GET"])
# def get_authors(request):
#     page = int(request.GET.get('page', '1'))
#     size = int(request.GET.get('size', '10'))
#     authors = Author.objects.all()
#     response = get_paginated_response(authors, page, size)
#     return Response(response)


# @api_view(["GET"])
# def get_followers(request, author_id):
#     page = int(request.GET.get('page', '1'))
#     size = int(request.GET.get('size', '10'))

#     followers = Follow.objects.get(
#         author=Author.objects.get(uuid=author_id).user)
#     response = get_paginated_response(followers, page, size)
#     return Response(response)


# @api_view(["GET"])
# def get_post(request, author_id, post_id):
#     post = get_object_or_404(Post, uuid=post_id)
#     if post.visibility != 'PUBLIC':
#         return Response({'error': 'Unauthorized'}, status=403)
#     return Response(post.get_json_object())


# @api_view(["GET"])
# def get_posts(request, author_id):
#     page = int(request.GET.get('page', '1'))
#     size = int(request.GET.get('size', '10'))
#     posts = Post.objects.filter(
#         visibility='PUBLIC', author=Author.objects.get(uuid=author_id).user)
#     response = get_paginated_response(posts, page, size)
#     return Response(response)


# @api_view(["POST"])
# def post_to_inbox(request, author_id):
#     return Response(response)
