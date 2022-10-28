from app.models import Author, Follower, Post
from rest_framework import serializers
from django.core.paginator import Paginator


def get_paginated_response(items, page, size):
    paginator = Paginator(items, size)
    page_obj = paginator.get_page(page)

    objects = []
    for object in page_obj.object_list:
        objects.append(object.get_json_object())

    res = {"type": objects[0]['type'] + 's', "page": page,
           "size": size, "items": objects}
    return res
