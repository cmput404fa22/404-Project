from django.urls import path
from .views import user, home, posts

urlpatterns = [
    path('', home.root, name='root-page'),
    path('login/', user.login_user, name='login-page'),
    path('logout/', user.logout_user, name='logout-page'),

    # path('author/', user.author, name='account-page'),
    path('signup/', user.signup, name='signup-page'),

    path('authorposts/', posts.list_posts, name='author-posts'),
    path('post/new/', posts.create_public_post, name='new-post-page'),
    path('post/edit/<str:post_url>/', posts.edit_post, name='edit-post-page'),

]
