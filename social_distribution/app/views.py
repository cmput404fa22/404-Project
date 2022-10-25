from re import U
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


def root(request):
    context = {"title": "root"}
    return render(request, "app/root.html", context)


def login(request):
    context = {"title": "login"}

    return render(request, "app/login.html", context)

def signup(request):
    context = {"title": "signup"}
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        github = request.POST['github']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email Taken')
            return redirect('signup-page')
        else:
            user = User.objects.create_user(email=email, password=password, username=username)
            user.save()
            user_model = User.objects.get(username=username)
            new_author = Author.objects.create(user=user_model, github=github, display_name=username)
            new_author.save()
            return redirect('login-page')
    else: 
        return render(request, "app/signup.html", context)

def account(request):
    context = {"title": "account"}
    return render(request, "app/account.html", context)
