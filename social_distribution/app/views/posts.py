from datetime import timezone
from django.shortcuts import render
from ..forms import CreatePostForm
from ..models import Post
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def send_private_post(request):
    pass


@login_required
def list_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {'posts': posts}
    return render(request, 'app/author_posts.html', context)


@login_required
def create_public_post(request):
    context = {"title": "create post", "form": CreatePostForm()}

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            new_post = Post.objects.create(title=form.cleaned_data['title'],
                                           description=form.cleaned_data['description'],
                                           content_type=form.cleaned_data['content_type'],
                                           content=form.cleaned_data['content'],
                                           author=request.user,
                                           visibility='PUBLIC',
                                           author_url=request.user.author.url)
            new_post.url = f'{request.user.author.url}/posts/{new_post.uuid.hex}'
            new_post.comments_url = f'{new_post.url}/comments'

            new_post.save()
            messages.success(request, 'Post created')

            return redirect('author-posts')

    return render(request, "app/create_post.html", context)


@login_required
def edit_post(request, uuid):
    context = {}
    form = CreatePostForm()
    post = Post.objects.get(uuid=uuid)

    if (post.author.user != request.user):
        return HttpResponse('Unauthorized', status=401)

    if request.method != 'POST':
        form = CreatePostForm(initial={"title": post.title,
                                       "description": post.description,
                                       "content_type": post.content_type,
                                       "content": post.content})

    else:
        form = CreatePostForm(request.POST, initial={"title": post.title,
                                                     "description": post.description,
                                                     "content_type": post.content_type,
                                                     "content": post.content})
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.description = form.cleaned_data['description']
            post.content_type = form.cleaned_data['content_type']
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('author-posts')

    context = {"post": post, "form": form}
    return render(request, 'app/edit_post.html', context)


@login_required
def delete_post(request, uuid):
    post = Post.objects.get(uuid=uuid)
    if (post.author.user != request.user):
        return HttpResponse('Unauthorized', status=401)

    post.delete()
    return redirect('author-posts')
