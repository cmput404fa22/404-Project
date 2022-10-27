from django.shortcuts import render
from ..forms import SendFriendRequestForm
from ..models import FriendRequest
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
            friend_request = FriendRequest(target=target,
                                           author=request.user)

            friend_request.save()
            messages.success(request, 'Friend request sent')

            return redirect('login-page')

    return render(request, "app/create_post.html", context)  # TODO: html
