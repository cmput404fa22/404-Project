from django.urls import path
from .views import user, home, posts

urlpatterns = [
    path('', home.root, name='root-page'),
    path('login/', user.login_user, name='login-page'),
    path('logout/', user.logout_user, name='logout-page'),

    # path('author/', user.author, name='account-page'),
    path('signup/', user.signup, name='signup-page'),
    path('profile/', user.profile, name='profile-page'),

    path('post/new/', posts.create_public_post, name='new-post-page'),

]
