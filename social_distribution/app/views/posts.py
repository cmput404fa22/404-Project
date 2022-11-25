from datetime import timezone
from django.shortcuts import render
from ..forms import CreatePostForm
from ..models import Post, Like, Follow, Author, InboxItem
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def send_private_post(request):
    pass


@login_required
def list_posts(request):
    # posts with received=True mean they were sent by another node to our author
    json_posts = []
    posts = Post.objects.filter(
        author=request.user.author, received=False)
    for post in posts:
        json_posts.append(post.get_json_object())

    context = {'posts': json_posts}
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
                                           author=request.user.author,
                                           visibility='PUBLIC',
                                           author_url=request.user.author.url,
                                           received=False)
            new_post.url = f'{request.user.author.url}/posts/{new_post.uuid.hex}'
            new_post.comments_url = f'{new_post.url}/comments'

            new_post.save()
            messages.success(request, 'Post created')

            # send posts to inbox of followers
            if new_post.visibility == 'PUBLIC':
                followers = Follow.objects.filter(author=request.user.author)
                for follower in followers:
                    follower_url = follower.target_url
                    follower_uuid = follower_url.split("/")[-1]
                    target = Author.objects.get(uuid=follower_uuid)
                    target_inbox_item = InboxItem.objects.create(
                        author=target, type="POST", from_author_url=request.user.author.url, from_username=request.user.username, object_url=new_post.url)
                    target_inbox_item.save()
            return redirect('author-posts')

    return render(request, "app/create_post.html", context)


@login_required
def edit_post(request, uuid):
    context = {}
    form = CreatePostForm()
    post = Post.objects.get(uuid=uuid, received=False)

    if (post.author != request.user.author):
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
    post = Post.objects.get(uuid=uuid, received=False)
    if (post.author != request.user.author):
        return HttpResponse('Unauthorized', status=401)

    post.delete()
    return redirect('author-posts')


@login_required
def like_post(request):
    user_url = request.user.author.url
    post_id = request.GET.get('post_id')
    post = Post.objects.get(uuid=post_id)

    like_filter = Like.objects.filter(post=post, liker_url=user_url)
    if not like_filter:
        new_like = Like.objects.create(liker_url=user_url, post=post)
        new_like.save()
        post.likes_count += 1
        post.save()

        target_inbox_item = InboxItem.objects.create(
            author=post.author, type="LIKE", from_author_url=request.user.author.url, from_username=request.user.username)
        target_inbox_item.save()

        messages.success(request, 'Liked post')
    else:
        return redirect('/')

    return redirect('/')
