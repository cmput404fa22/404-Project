from django.urls import path, register_converter
from . import views
from .converters import UUIDConverter


# https://docs.djangoproject.com/en/3.2/topics/http/urls/#registering-custom-path-converters
register_converter(UUIDConverter, 'uuid')

urlpatterns = [
    path("", views.get_authors),
    path("<uuid:author_id>/", views.get_author),
    # path("<uuid:author_id>/followers", views.get_followers),

    path("<uuid:author_id>/posts/<uuid:post_id>", views.get_post),
    path("<uuid:author_id>/posts/", views.get_posts),

    # path("<uuid:author_id>/inbox/", views.post_to_inbox),


]
