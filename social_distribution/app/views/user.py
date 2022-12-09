from multiprocessing import context
from re import U
from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from django.contrib import messages
from django.shortcuts import redirect
from ..forms import SignupForm, LoginForm, UserUpdateForm, AuthorUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..utils import url_is_local
from ..connections.teams import RemoteNodeConnection
import requests


def signup(request):
    context = {"title": "signup", "form": SignupForm(
    ), "has_author": hasattr(request.user, 'author')}

    if (request.user.is_authenticated):
        logout_user(request)

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
                new_author.url = f'{new_author.host}/authors/{new_author.uuid.hex}'
                if form.cleaned_data['github']:
                    new_author.github = form.cleaned_data['github']
                new_author.save()

            return redirect('login-page')

    return render(request, "app/signup.html", context)


def login_user(request):
    context = {"title": "login", "form": LoginForm(
    ), "has_author": hasattr(request.user, 'author')}

    if (request.user.is_authenticated):
        logout_user(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user and hasattr(user, 'author') and user.author.registered:
                login(request, user)
                messages.success(request, 'Logged in')
                return redirect('stream')
            else:
                messages.error(request, "Could not authenticate")
                return redirect('login-page')

    return render(request, "app/login.html", context)


def logout_user(request):
    logout(request)

    return redirect('login-page')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        author_form = AuthorUpdateForm(
            request.POST, request.FILES, instance=request.user.author)

        if user_form.is_valid() and author_form.is_valid():
            user_form.save()
            author_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile-page')
    else:
        user_form = UserUpdateForm(instance=request.user)
        author_form = AuthorUpdateForm(instance=request.user.author)

    context = {
        'user_form': user_form,
        'author_form': author_form,
        "has_author": hasattr(request.user, 'author')
    }

    return render(request, 'app/profile.html', context)


@login_required
def public_profile(request):
    author_url = request.GET.get('author_url', '')
    if (author_url == ""):
        return HttpResponse('400: No author_url query parameter supplied', status=400)

    if url_is_local(author_url):
        uuid = author_url.split("/")[-1]
        author = Author.objects.get(uuid=uuid)
        github_name = author.github.split('/')[-1]
        follows_you = Follow.objects.filter(
            author=request.user.author, target_url=author.url).first()
        posts = Post.objects.filter(
            author=author, visibility='PUBLIC', received=False, unlisted=False)

        authors_posts = []
        for p in posts:
            post = p.get_json_object()
            post["image"] = p.image
            post["date"] = p.date_published.strftime('%Y-%m-%d %H:%M')
            authors_posts.append(post)

        author = author.get_json_object()

    else:
        uuid = author_url.split("/")[-1]
        remote_node_conn = RemoteNodeConnection(author_url)
        try:
            author = remote_node_conn.conn.get_author(uuid)
            follows_you = Follow.objects.filter(
                author=request.user.author, target_url=author['url']).first()
            authors_posts = remote_node_conn.conn.get_all_authors_posts(
                author_url.split("/")[-1])
        except Exception as e:
            messages.warning(request, str(e))
            follows_you = False
            authors_posts = []

    github_events = []
    if author['github']:
        github_name = author['github'].split('/')[-1]
        git_url = f"https://api.github.com/users/{github_name}/events/public"
        github_response = requests.get(git_url)

        if github_response.status_code == 200:
            github_response = github_response.json()
            for github_post in github_response:
                github_event = {"type": github_post['type'], "repo": github_post['repo']['name'],
                                "time": github_post['created_at']}
                github_events.append(github_event)

    context = {"author": author,
               "follows_you": follows_you, "posts": authors_posts, "github_events": github_events, "has_author": hasattr(request.user, 'author')}
    return render(request, 'app/public_profile.html', context)


@login_required
def notifications(request):
    notifs = InboxItem.objects.filter(
        author=request.user.author).order_by("-date_published")

    context = {"notifs": notifs, "has_author": hasattr(request.user, 'author')}
    return render(request, 'app/notifications.html', context)
