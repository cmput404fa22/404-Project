from datetime import timezone
from django.shortcuts import render
from ..forms import CreatePostForm, SharePostForm
from ..models import Post, Like, Follow, Author, InboxItem
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..utils import url_is_local
from ..connections.teams import RemoteNodeConnection
from django.http import JsonResponse


def send_private_post(request):
    pass


@login_required
def list_posts(request):
    # posts with received=True mean they were sent by another node to our author
    json_posts = []
    posts = Post.objects.filter(
        author=request.user.author, received=False).order_by("-date_published")
    for post in posts:
        json_posts.append(post.get_json_object())

    context = {'posts': json_posts}
    return render(request, 'app/author_posts.html', context)


@login_required
def create_public_post(request):
    context = {"title": "create post",
               "form": CreatePostForm(request.user.author)}

    if request.method == 'POST':
        form = CreatePostForm(request.user.author, request.POST)
        if form.is_valid():
            if list(form.cleaned_data['followers']) == []:
                visibility = 'PUBLIC'
            else:
                visibility = 'FRIENDS'

            new_post = Post.objects.create(title=form.cleaned_data['title'],
                                           description=form.cleaned_data['description'],
                                           content_type=form.cleaned_data['content_type'],
                                           content=form.cleaned_data['content'],
                                           unlisted=form.cleaned_data['unlisted'],
                                           author=request.user.author,
                                           visibility=visibility,
                                           author_url=request.user.author.url,
                                           received=False)
            new_post.url = f'{request.user.author.url}/posts/{new_post.uuid.hex}'
            new_post.comments_url = f'{new_post.url}/comments'

            new_post.save()
            messages.success(request, 'Post created')

            # send posts to inbox of followers
            if new_post.visibility == 'PUBLIC':
                followers_to_send_to = Follow.objects.filter(
                    author=request.user.author, accepted=True)
            else:
                followers_to_send_to = form.cleaned_data['followers']

            for follower in followers_to_send_to:
                follower_url = follower.target_url
                follower_uuid = follower_url.split("/")[-1]
                if url_is_local(follower_url):
                    author_to_send_to = Author.objects.get(uuid=follower_uuid)
                    inbox_item = InboxItem.objects.create(
                        author=author_to_send_to, type="POST", from_author_url=request.user.author.url, from_username=request.user.username, object_url=new_post.url)
                    inbox_item.save()
                else:
                    try:
                        remote_node_conn = RemoteNodeConnection(follower_url)
                        remote_node_conn.conn.send_post(
                            new_post, follower_uuid)
                    except Exception as e:
                        messages.error(
                            request, f"Could not send post to {follower_url}. Error: {e}")
                        print(e)

            return redirect('author-posts')

    return render(request, "app/create_post.html", context)


@login_required
def edit_post(request, uuid):
    context = {}
    post = Post.objects.get(uuid=uuid, received=False)
    form = CreatePostForm(post.author)

    if (post.author != request.user.author):
        return HttpResponse('Unauthorized', status=401)

    if request.method != 'POST':
        form = CreatePostForm(post.author, initial={"title": post.title,
                                                    "description": post.description,
                                                    "content_type": post.content_type,
                                                    "content": post.content,
                                                    "unlisted": post.unlisted})

    else:
        form = CreatePostForm(post.author, request.POST, initial={"title": post.title,
                                                                  "description": post.description,
                                                                  "content_type": post.content_type,
                                                                  "content": post.content,
                                                                  "unlisted": post.unlisted})
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.description = form.cleaned_data['description']
            post.content_type = form.cleaned_data['content_type']
            post.content = form.cleaned_data['content']
            post.unlisted = form.cleaned_data['unlisted']
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


@login_required
def share_post(request):
    form = SharePostForm(request.user.author)
    return render(request, 'app/share_post.html', {"share_form": form})


@login_required
def submit_share_post_form(request):
    form = SharePostForm(request.user.author)
    post_id = request.GET.get('post_id')
    post = Post.objects.get(uuid=post_id)

    if request.method == 'POST':
        form = SharePostForm(request.user.author, request.POST)
        if form.is_valid():
            response = JsonResponse({"message": 'success'})
            response.status_code = 201
            # send post to inbox of followers

            followers_to_send_to = form.cleaned_data['followers']

            for follower in followers_to_send_to:
                follower_url = follower.target_url
                follower_uuid = follower_url.split("/")[-1]
                if url_is_local(follower_url):
                    author_to_send_to = Author.objects.get(uuid=follower_uuid)
                    inbox_item = InboxItem.objects.create(
                        author=author_to_send_to, type="POST", from_author_url=request.user.author.url, from_username=request.user.username, object_url=post.url)
                    inbox_item.save()
                else:
                    try:
                        remote_node_conn = RemoteNodeConnection(follower_url)
                        remote_node_conn.conn.send_post(
                            post, follower_uuid)
                    except Exception as e:
                        messages.error(
                            request, 'Could not send post to all selected followers :(')
                        print(e)
        else:
            response = JsonResponse({"errors": form.errors.as_json()})
            response.status_code = 403
    return response


@login_required
def view_post(request):
    posts = []
    post_url = request.GET.get('post_url')
    post = Post.objects.get(url=post_url)
    posts.append(post)
    print(dir(posts[0]))
    return render(request, 'app/view_post.html', {"posts": posts})
