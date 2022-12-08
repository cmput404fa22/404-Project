from django.forms import ModelMultipleChoiceField
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import *
from .connections.teams import RemoteNodeConnection
from .utils import url_is_local


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)
    username = forms.CharField(label='Username', max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class AuthorUpdateForm(forms.ModelForm):
    github = forms.CharField(label='Github url', required=False)
    profile_image_url = forms.CharField(
        label='Profile image url', required=False)

    class Meta:
        model = Author
        fields = ['github', 'profile_image_url']


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True)
    github = forms.CharField(label='Github url', required=False)


class RemoteNodeSignupForm(forms.Form):
    team = forms.IntegerField(label='Team #', required=True)
    base_url = forms.CharField(label='Base URL', required=True)
    home_page = forms.CharField(label='Home page', required=True)
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True)
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=True)


class FollowModelChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, follow):
        follower_url = follow.target_url
        follower_uuid = follow.target_url.split("/")[-1]
        if url_is_local(follower_url):
            follower_author = Author.objects.get(uuid=follower_uuid)
            return f"{follower_author.user.username} ({follower_author.host})"
        else:
            remote_node_conn = RemoteNodeConnection(follower_url)
        try:
            author = remote_node_conn.conn.get_author(follower_uuid)
            return f"{author['displayName']} (REMOTE)"

        except Exception as e:
            print(e)

        return follower_url


class SharePostForm(forms.Form):
    def __init__(self, author, *args, **kwargs):
        super(SharePostForm, self).__init__(*args, **kwargs)
        self.fields['followers'] = FollowModelChoiceField(
            queryset=Follow.objects.filter(author=author, accepted=True),
            to_field_name="target_url",
            required=False,
        )


class CreatePostForm(forms.Form):
    def __init__(self, author, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['followers'] = FollowModelChoiceField(
            queryset=Follow.objects.filter(author=author, accepted=True),
            to_field_name="target_url",
            required=False,
            label='Send to Followers: (public if none selected)'
        )

    title = forms.CharField(label='Title', max_length=50, required=True)
    description = forms.CharField(
        label='Description', max_length=50, required=False)
    CONTENT_TYPE_CHOICES = (
        ("text/markdown", "text/markdown"),
        ("text/plain", "text/plain"),
        # ("image/png;base64", "image/png"),
        # ("image/jpeg;base64", "image/jpeg"),
    )
    content_type = forms.ChoiceField(
        choices=CONTENT_TYPE_CHOICES, label="Content type", initial='', widget=forms.Select(), required=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}),
                              label='Content', required=False)

    image = forms.FileField(required=False)

    unlisted = forms.BooleanField(widget=forms.CheckboxInput(
    ), label='Unlisted', initial=False, required=False)
