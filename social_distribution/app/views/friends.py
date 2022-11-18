from django.conf import settings
from django.shortcuts import render
from ..models import Follow, Author, InboxItem
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from uuid import UUID


@login_required
def follow(request):

    # get target
    target_url = request.GET.get('target_url', '')

    # check user url provided, if on our server save follow
    if (target_url.startswith("http://" + (settings.HOSTNAME or "")):  # TODO: FIX LATER TO PROPERLY CHECK!!!
        target_uuid = target_url.split("/")[-1]
        target = Author.objects.get(uuid=target_uuid)

        new_follow = Follow.objects.create(
            author=request.user, target_url=target.url)
        new_follow.save()

        target_inbox_item = InboxItem.objects.create(
            author=target, type="FOLLOW", from_author_url=request.user.author.url, from_username=request.user.username)
        target_inbox_item.save()

        messages.success(request, 'Requested to follow ' +
                         target.user.username)

    else:
        # TODO: post follow to remote node's inbox
        return

    return redirect('root-page')


@login_required
def approve_follow(request, uuid):

    # query followers table for unapproved follow request for our author

    # display

    return render(request, "app/respond_friend_request.html", context)
