from drf_yasg import openapi
from drf_yasg.views import get_schema_view
# from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from django.urls import path, register_converter, re_path
from . import views
from .converters import UUIDConverter
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Social Distribution API Doc",
        default_version='v1',
        description="Follow steps here: https://github.com/cmput404fa22/404-Project#remote-connections to register your node.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# https://docs.djangoproject.com/en/3.2/topics/http/urls/#registering-custom-path-converters
register_converter(UUIDConverter, 'uuid')

urlpatterns = [
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path("", views.AuthorItems.as_view()),
    path("<uuid:uuid>/", views.SingleAuthor.as_view()),
    path("<uuid:author_id>/followers", views.FollowItems.as_view()),

    path("all/posts/", views.AllPostItems.as_view()),
    path("<uuid:author_id>/posts/", views.PostItems.as_view()),
    path("<uuid:author_id>/posts/<uuid:post_id>", views.SinglePost.as_view()),
    path("<uuid:author_id>/posts/<uuid:post_id>/image",
         views.image_post, name='image'),

    path("<uuid:author_id>/inbox/", views.inbox_item),
]
