from re import U
from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from django.contrib import messages
from django.shortcuts import redirect
from ..forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
import os


def signup(request):
    context = {"title": "signup", "form": SignupForm()}

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup-page')

            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup-page')

            else:
                user = User.objects.create_user(email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'],
                                                username=form.cleaned_data['username'])
                new_author = Author(user=user)
                new_author.url = f'http://{new_author.host}/authors/{new_author.uuid.hex}'
                if form.cleaned_data['github']:
                    new_author.github = form.cleaned_data['github']
                new_author.save()

            return redirect('login-page')

    return render(request, "app/signup.html", context)


def login_user(request):
    context = {"title": "login", "form": LoginForm()}

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in')
                return redirect('author-posts')
            else:
                messages.error(request, "Could not authenticate")
                return redirect('login-page')

    return render(request, "app/login.html", context)


def logout_user(request):
    logout(request)

    return redirect('root-page')
