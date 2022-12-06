from django.conf import settings
from django.shortcuts import render
from ..models import Follow, Author, InboxItem
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from uuid import UUID
from ..utils import url_is_local
from django.http import HttpResponse
from ..connections.teams import RemoteNodeConnection


@login_required
def follow(request):
    # get target
    target_url = request.GET.get('target_url', '')
    target_uuid = target_url.split("/")[-1]

    # check user url provided, if on our server save follow
    if url_is_local(target_url):
        target = Author.objects.get(uuid=target_uuid)

        new_follow = Follow.objects.create(
            author=target, target_url=request.user.author.url)
        new_follow.save()

        target_inbox_item = InboxItem.objects.create(
            author=target, type="FOLLOW", from_author_url=request.user.author.url, from_username=request.user.username)
        target_inbox_item.save()
        messages.success(request, 'Follow request sent')

    else:
        remote_node_conn = RemoteNodeConnection(target_url)
        try:
            followed = remote_node_conn.conn.send_follow_request(
                request.user.author, target_uuid)
            messages.success(request, 'Follow request sent')
        except Exception as e:
            messages.warning(request, str(e))

    return redirect('/public_profile/?author_url=' + target_url)


@login_required
def approve_follow(request, inbox_item_id):

    inbox_item = InboxItem.objects.get(uuid=inbox_item_id)
    follow = Follow.objects.filter(
        target_url=inbox_item.from_author_url).first()
    if follow and follow.author != request.user.author:
        return HttpResponse('Unauthorized', status=401)

    follow.accepted = True
    follow.save()
    inbox_item.delete()

    messages.success(
        request, f"Accepted {inbox_item.from_username}'s follow request")

    return redirect('notifications-page')


@login_required
def reject_follow(request, inbox_item_id):

    inbox_item = InboxItem.objects.get(uuid=inbox_item_id)
    follow = Follow.objects.filter(
        target_url=inbox_item.from_author_url).first()
    if follow and follow.author != request.user.author:
        return HttpResponse('Unauthorized', status=401)

    follow.delete()
    inbox_item.delete()

    messages.success(
        request, f"Deleted {inbox_item.from_username}'s follow request")

    return redirect('notifications-page')
