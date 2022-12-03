from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from app.models import InboxItem, Author, RemoteNode, Post
from django.db.models import Q
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from ..connections.teams import RemoteNodeConnection


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
        except Exception:
            authors = []
        other_node = {"home_page": node.home_page,
                      "posts": posts, "authors": authors}
        other_nodes.append(other_node)

    local_posts = []
    posts = Post.objects.filter(
        visibility="PUBLIC", received=False)[:5]
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
        posts = InboxItem.get_posts(
            author=request.user.author, num_of_posts=size, page=page)
    except EmptyPage:
        posts = []

    # ~Q negates
    other_author = Author.objects.filter(
        ~Q(uuid=request.user.author.uuid), registered=True).first()

    context = {"paginated_posts": {"posts": posts, "page": page,
                                   "size": size}, "other_author": other_author}
    return render(request, "app/stream.html", context)
