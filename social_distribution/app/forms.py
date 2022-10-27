from urllib import request
from django import forms
from .models import Follower


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True)
    github = forms.CharField(label='Github url', required=False)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True)


class CreatePostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50, required=True)
    description = forms.CharField(
        label='Description', max_length=50, required=False)

    CONENT_TYPE_CHOICES = (
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        ("image", "image"),
    )
    content_type = forms.ChoiceField(
        choices=CONENT_TYPE_CHOICES, label="Content type", initial='', widget=forms.Select(), required=True)
    content = forms.CharField(
        label='Content', widget=forms.TextInput(attrs={'': ''}))

class SendFriendRequestForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)