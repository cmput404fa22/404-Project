from django.shortcuts import render
from ..forms import CreatePostForm
from ..models import Post
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def send_private_post(request):
    pass


@login_required
def create_public_post(request):
    context = {"title": "create post", "form": CreatePostForm()}

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            content_type=form.cleaned_data['content_type'],
                            content=form.cleaned_data['content_type'],
                            author=request.user,
                            visibility='PUBLIC',
                            source=request.user.author.host,
                            origin=request.user.author.host,
                            author_url=request.user.author.url)
            new_post.url = f'{request.user.author.url}/posts/{new_post.uuid.hex}'
            new_post.comments_url = f'{new_post.url}/comments'

            new_post.save()
            messages.success(request, 'Post created')

            return redirect('login-page')

    return render(request, "app/create_post.html", context)
