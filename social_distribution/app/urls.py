from django.urls import path, register_converter
from .views import user, home, posts, friends
from api.converters import UUIDConverter

register_converter(UUIDConverter, 'uuid')


urlpatterns = [
    path('', home.root, name='root-page'),
    path('login/', user.login_user, name='login-page'),
    path('logout/', user.logout_user, name='logout-page'),

    # path('author/', user.author, name='account-page'),
    path('signup/', user.signup, name='signup-page'),
    path('profile/', user.profile, name='profile-page'),
    path('notifications/', user.notifications, name='notifications-page'),
    path('public_profile/', user.public_profile, name='public-profile-page'),

    path('authorposts/', posts.list_posts, name='author-posts'),
    path('authorposts/new/', posts.create_public_post, name='new-post-page'),
    path('authorposts/edit/<uuid:uuid>', posts.edit_post, name='edit-post-page'),
    path('authorposts/delete/<uuid:uuid>', posts.delete_post, name='delete'),

    path('follow/user/', friends.follow, name='follow_user'),
    path('follow/approve/<uuid:inbox_item_id>',
         friends.approve_follow, name='approve_follow'),
    path('follow/reject/<uuid:inbox_item_id>',
         friends.reject_follow, name='reject_follow'),
    path('stream/', home.stream, name='stream'),

]
