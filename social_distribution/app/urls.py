from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root-page'),
    path('login/', views.login, name='login-page'),
    path('account/', views.account, name='account-page'),
    path('signup/', views.signup, name='signup-page'),
]
