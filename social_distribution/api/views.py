from .serializers import AuthorSerializer, PostSerializer
from app.models import Author, Post, Follow, InboxItem
from app.utils import url_is_local
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, status
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings


class AuthorItems(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': AuthorSerializer})
    def get(self, request):
        authors = Author.objects.all()

        results = self.paginate_queryset(authors, request, view=self)
        serializer = AuthorSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class FollowItems(APIView, LimitOffsetPagination):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(responses={'200': AuthorSerializer})
    def get(self, request, author_id):
        author = Author.objects.get(uuid=author_id)
        follows = Follow.objects.filter(author=author)

        authors = []
        follow_urls = self.paginate_queryset(follows, request, view=self)
        for follow in follow_urls:
            if url_is_local(follow.target_url):
                author = Author.objects.get(
                    uuid=follow.target_url.split("/")[-1])
                authors.append(author)
            else:
                continue
                # TODO get from remote node

        serializer = AuthorSerializer(authors, many=True)
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
        author = Author.objects.get(uuid=author_id)
        posts = Post.objects.filter(author=author)

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


@api_view(['POST'])
def inbox_item(request, author_id):
    author = Author.objects.get(uuid=author_id)

    for item in request.data.get("items"):
        if (item.get("type") == 'post'):
            serializer = PostSerializer(data=item)
            if serializer.is_valid():
                # only save posts with FRIENDS visibility,
                # PUBLIC posts can be retrieved from remote nodes when needed
                if (serializer.validated_data.get('visibility') == 'FRIENDS'):
                    post = serializer.create(
                        serializer.validated_data, author=author)
                    post.received = True
                    post.save()
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        if (item.get("type") == 'follow'):
            return Response({"posting follows is not implemented yet"}, status.HTTP_501_NOT_IMPLEMENTED)

        if (item.get("type") == 'comment'):
            return Response({"posting comments is not implemented yet"}, status.HTTP_501_NOT_IMPLEMENTED)

        if (item.get("type") == 'like'):
            return Response({"posting likes is not implemented yet"}, status.HTTP_501_NOT_IMPLEMENTED)

            # TODO: Get username for this author request.data.get("author")

        inbox_item = InboxItem.objects.create(
            author=author,
            type=item.get("type").upper(),
            from_author_url=request.data.get("author"),
            object_url=serializer.validated_data.get('url'),
            from_username="TODO: add username")
        inbox_item.save()

        return Response("Inbox item received", status.HTTP_201_CREATED)

    return Response({})
