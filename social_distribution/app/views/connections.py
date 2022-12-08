from multiprocessing import context
from re import U
from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from django.contrib import messages
from django.shortcuts import redirect
from ..forms import RemoteNodeSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from uuid import UUID
from ..utils import url_is_local


def signup_remote_node(request):
    context = {"title": "signup", "form": RemoteNodeSignupForm(), "has_author": hasattr(request.user, 'author')}

    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = RemoteNodeSignupForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup-page')

            else:
                user = User.objects.create_user(password=form.cleaned_data['password'],
                                                username=form.cleaned_data['username'])
                node = RemoteNode.objects.create(
                    user=user,
                    base_url=form.cleaned_data['base_url'],
                    home_page=form.cleaned_data['home_page'],
                    team=form.cleaned_data['team'])
                node.save()

            return redirect('schema-swagger-ui')

    return render(request, "app/signup.html", context)
