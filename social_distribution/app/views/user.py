from re import U
from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from django.contrib import messages
from django.shortcuts import redirect
from ..forms import SignupForm, LoginForm, UserUpdateForm, AuthorUpdateForm
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

    return redirect('login-page')

def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance = request.user)
        author_form = AuthorUpdateForm(request.POST, request.FILES, instance = request.user.author)
        
        if user_form.is_valid() and author_form.is_valid():
            user_form.save()
            author_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile-page')
    else:
        user_form = UserUpdateForm(instance = request.user)
        author_form = AuthorUpdateForm(instance = request.user.author)

    context = {
        'user_form': user_form,
        'author_form': author_form
    }

    return render(request, 'app/profile.html', context)