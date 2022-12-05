from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from app.models import InboxItem, Author, RemoteNode, Post
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from ..connections.teams import RemoteNodeConnection
from ..utils import url_is_local


def root(request):

    other_nodes = []
    remote_nodes = RemoteNode.objects.filter(registered=True)
    for node in remote_nodes:
        remote_node_conn = RemoteNodeConnection(node.base_url)
        # TODO: get public posts for this node
        posts = []
        # get all the node's authors
        try:
            authors = remote_node_conn.conn.get_all_authors()[:5]
        except Exception as e:
            print(e)
            authors = []
        other_node = {"home_page": node.home_page,
                      "posts": posts, "authors": authors}
        other_nodes.append(other_node)

    local_posts = []
    posts = Post.objects.filter(
        visibility="PUBLIC", received=False).order_by("-date_published")[:5]
    for post in posts:
        local_posts.append(post.get_json_object())

    context = {"title": "root", "nodes": other_nodes,
               "local_url": settings.HOSTNAME, "local_posts": local_posts}
    return render(request, "app/root.html", context)


@login_required
def stream(request):
    page = int(request.GET.get('page', '1'))
    size = int(request.GET.get('size', '10'))

    try:
        posts = get_posts_from_inbox(
            author=request.user.author, num_of_posts=size, page=page)
    except EmptyPage:
        posts = []

    # ~Q negates
    other_author = Author.objects.filter(
        ~Q(uuid=request.user.author.uuid), registered=True).first()

    context = {"paginated_posts": {"posts": posts, "page": page,
                                   "size": size}, "other_author": other_author}
    return render(request, "app/stream.html", context)


def get_posts_from_inbox(author, num_of_posts, page):
    posts = InboxItem.objects.filter(
        author=author, type="POST").order_by('-date_published')
    paginator = Paginator(posts, num_of_posts)
    page = paginator.page(page)

    post_objects = []
    for item in page:
        url = item.object_url
        uuid = url.split("/")[-1]
        received_post = Post.objects.filter(uuid=uuid).first()
        if url_is_local(url) and received_post == None:
            post = Post.objects.get(uuid=uuid)
            post_objects.append(post.get_json_object())
        elif received_post:
            post = Post.objects.get(uuid=uuid).get_json_object()
            post["author"]["id"] = item.from_author_url
            post["author"]["displayName"] = item.from_username
            post["received"] = True
            post_objects.append(post)
        else:
            try:
                author_uuid = item.from_author_url
                remote_node_conn = RemoteNodeConnection(item.object_url)
                post = remote_node_conn.get_post(
                    author_uuid=author_uuid, post_uuid=uuid)
                post_objects.append(post)
            except Exception as e:
                print(e)

    return post_objects
