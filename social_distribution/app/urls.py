from django.urls import path
from .views import user, home, posts

urlpatterns = [
    path('', home.root, name='root-page'),
    path('login/', user.login_user, name='login-page'),
    path('logout/', user.logout_user, name='logout-page'),

    # path('author/', user.author, name='account-page'),
    path('signup/', user.signup, name='signup-page'),

    path('authorposts/', posts.list_posts, name='author-posts'),
    path('authorposts/new/', posts.create_public_post, name='new-post-page'),
    path('authorposts/edit/<uuid:uuid>', posts.edit_post, name='edit-post-page'),
    path('authorposts/delete/<uuid:uuid>', posts.delete_post, name='delete')

]
