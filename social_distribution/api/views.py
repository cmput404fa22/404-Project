from .serializers import AuthorSerializer, PostSerializer
from app.models import Author, Post, Follow, InboxItem
from app.utils import url_is_local, clean_url
from urllib import response
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView, status
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRemoteNode
from .swagger import CustomSwaggerAutoSchema
from app.connections.teams import RemoteNodeConnection
from django.http import HttpResponse
import base64
from drf_yasg import openapi


# @api_view(['GET'])
# @permission_classes([IsAuthenticated, IsRemoteNode])
# @swagger_auto_schema(responses={'200': openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE))}, produces='application/octet-stream')
# def image_post(request, uuid):
#     post = Post.objects.get(uuid=uuid, received=False)
#     image_bytes = str.encode(post.image)
#     return HttpResponse(base64.decodebytes(image_bytes), content_type=post.content_type)


class Image(APIView):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(responses={'200': openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE))}, produces='application/octet-stream')
    def get(self, request, author_id, uuid):
        post = Post.objects.get(uuid=uuid, received=False)
        image_bytes = str.encode(post.image)
        return HttpResponse(base64.decodebytes(image_bytes), content_type=post.content_type)


class AuthorItems(APIView, LimitOffsetPagination):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(
        auto_schema=CustomSwaggerAutoSchema,
        responses={200: AuthorSerializer(many=True)},
        paginator=LimitOffsetPagination()
    )
    def get(self, request):
        authors = Author.objects.filter(registered=True)

        results = self.paginate_queryset(authors, request, view=self)
        serializer = AuthorSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class FollowItems(APIView, LimitOffsetPagination):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(
        auto_schema=CustomSwaggerAutoSchema,
        responses={200: AuthorSerializer(many=True)},
        paginator=LimitOffsetPagination()
    )
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

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(responses={'200': AuthorSerializer})
    def get(self, request, uuid):
        author = Author.objects.get(uuid=uuid)
        serializer = AuthorSerializer(author, many=False)
        return Response(serializer.data)


class PostItems(APIView, LimitOffsetPagination):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(
        auto_schema=CustomSwaggerAutoSchema,
        responses={200: PostSerializer(many=True)},
        paginator=LimitOffsetPagination()
    )
    def get(self, request, author_id):
        author = Author.objects.get(uuid=author_id)
        posts = Post.objects.filter(author=author, visibility='PUBLIC')

        results = self.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class AllPostItems(APIView, LimitOffsetPagination):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(
        auto_schema=CustomSwaggerAutoSchema,
        responses={200: PostSerializer(many=True)},
        paginator=LimitOffsetPagination()
    )
    def get(self, request):
        posts = Post.objects.filter(visibility='PUBLIC')

        results = self.paginate_queryset(posts, request, view=self)
        serializer = PostSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class SinglePost(APIView, LimitOffsetPagination):

    permission_classes = [IsAuthenticated, IsRemoteNode]

    @swagger_auto_schema(responses={'200': PostSerializer})
    def get(self, request, author_id, post_id):
        post = Post.objects.get(uuid=post_id)
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)


@swagger_auto_schema(methods=['post'], operation_description="**NOTE** This endpoint expects JSON in the request body to be in the same format as: https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/project.org#inbox ")
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRemoteNode])
def inbox_item(request, author_id):
    author = Author.objects.get(uuid=author_id)

    from_author = request.data.get("author")
    items = request.data.get("items")
    if (items == None or from_author == None):
        return Response("Bad request", status.HTTP_400_BAD_REQUEST)

    from_author_url = clean_url(from_author)
    from_username = ""
    new_objects = []
    friends_post = None
    for item in items:
        if (item.get("type") == 'post'):

            serializer = PostSerializer(data=item)
            if (not serializer.is_valid()):
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            object_url = clean_url(serializer.validated_data.get("url"))

            # only save posts with FRIENDS visibility,
            # PUBLIC posts can be retrieved from remote nodes when needed
            if (serializer.validated_data.get('visibility') == 'FRIENDS'):
                post = serializer.create(
                    serializer.validated_data, author=author)
                post.received = True
                friends_post = post
                new_objects.append(post)

        if (item.get("type") == 'Follow'):

            serializer = AuthorSerializer(data=item.get('object'))
            if (not serializer.is_valid()):
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            from_username = item['actor']['displayName']
            author_uuid = serializer.validated_data.get("url").split("/")[-1]
            object_url = "follow"

            followed = Author.objects.get(uuid=author_uuid)
            follow = Follow.objects.create(
                author=followed, target_url=from_author_url)
            new_objects.append(follow)

        if (item.get("type") == 'comment'):
            return Response({"posting comments is not implemented yet"}, status.HTTP_501_NOT_IMPLEMENTED)

        if (item.get("type") == 'like'):
            return Response({"posting likes is not implemented yet"}, status.HTTP_501_NOT_IMPLEMENTED)

        if from_username == "":
            try:
                author_uuid = from_author_url.split("/")[-1]
                remote_node_conn = RemoteNodeConnection(from_author_url)
                author = remote_node_conn.conn.get_author(author_uuid)
                from_username = author["displayName"]
            except Exception as e:
                from_username = "Unknown"
                print(e)

        inbox_item = InboxItem.objects.create(
            author=author,
            type=item.get("type").upper(),
            from_author_url=from_author_url,
            object_url=object_url,
            from_username=from_username,
            friends_post=friends_post)
        new_objects.append(inbox_item)

    for obj in new_objects:
        obj.save()

    return Response("Inbox items received", status.HTTP_201_CREATED)
