from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)
    username = forms.CharField(label='Username', max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class AuthorUpdateForm(forms.ModelForm):
    github = forms.CharField(label='Github url', required=False)
    profile_image_url = forms.CharField(label='Profile image url', required=False)

    class Meta:
        model = Author
        fields = ['github', 'profile_image_url']

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
