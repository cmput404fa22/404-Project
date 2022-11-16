from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Author


# Create your tests here.
# run with python manage.py test

class UserModelTest(TestCase):  # base Django User

    def test_create_user(self):
        username = "name"
        password = "1234"
        user = get_user_model().objects.create_user(username=username, password=password)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))  # hashed


class AuthorModelTest(TestCase):  # our Author

    def setUp(self):
        username = "name"
        password = "1234"
        self.host = "localhost"
        self.url = "zombo.com"
        self.github = "github.com"
        self.profile_image_url = "9gag.com"
        user = get_user_model().objects.create_user(username=username, password=password)
        Author.objects.create(user=user,
                              host=self.host,
                              url=self.url,
                              github=self.github,
                              profile_image_url=self.profile_image_url)
        self.author = Author.objects.get(user=user)

    def test_create_author(self):
        self.assertTrue(self.author)  # author created

    def test_author_not_registered(self):
        self.assertFalse(self.author.registered)  # admin has not registered author

    def test_links(self):
        self.assertEqual(self.author.host, self.host)
        self.assertEqual(self.author.url, self.url)
        self.assertEqual(self.author.github, self.github)
        self.assertEqual(self.author.profile_image_url, self.profile_image_url)
