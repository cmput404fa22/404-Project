from django.shortcuts import render
from ..forms import SendFriendRequestForm, RespondFriendRequestForm
from ..models import FriendRequest, Follower
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def send_friend_request(request):
    context = {"title": "send friend request", "form": SendFriendRequestForm()}

    if request.method == 'POST':
        form = SendFriendRequestForm(request.POST)
        if form.is_valid():
            target = User.objects.filter(username=form.cleaned_data['username']).first()
            friend_request = FriendRequest.objects.create(target=target,
                                                          author=request.user)

            friend_request.save()
            messages.success(request, 'Friend request sent')

            return redirect('root-page')

    return render(request, "app/send_friend_request.html", context)


@login_required
def respond_friend_request(request, author):
    context = {"title": "respond to friend request", "form": RespondFriendRequestForm()}

    if request.method == 'POST':
        form = RespondFriendRequestForm(request.POST)
        if form.is_valid():
            friend_request = FriendRequest.objects.get(target=request.user, author=author)
            if form.cleaned_data['response'] == 'accept':
                follower = Follower(author=request.user, follower_url=author.url)  # syntax?
                # opposite semantics, author is who is being friended
                follower.save()
                messages.success(request, 'Friend request accepted!')
                friend_request.delete()
            elif form.cleaned_data['response'] == 'reject':
                friend_request.delete()
                messages.success(request, 'Friend request rejected!')

            return redirect('root-page')

    return render(request, "app/respond_friend_request.html", context)
