from django.shortcuts import render


def root(request):
    context = {"title": "root"}
    return render(request, "app/root.html", context)
