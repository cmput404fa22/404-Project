from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def root(request):
    context = {"title": "root"}
    return render(request, "app/root.html", context)


def login(request):
    context = {"title": "login"}
    return render(request, "app/login.html", context)


def account(request):
    context = {"title": "account"}
    return render(request, "app/account.html", context)
