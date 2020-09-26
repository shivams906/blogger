from django.test import TestCase
from django.contrib.auth import get_user_model
from blogger.models import Post, Author
from blogger.forms import PostModelForm

User = get_user_model()


class PostModelFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user", password="top_secret")
        cls.author = Author.objects.create(user=user)

    def test_valid_data_creates_post(self):
        form = PostModelForm({"title": "title", "content": "content"})
        if form.is_valid():
            form.save(author=self.author)
        self.assertEqual(Post.objects.count(), 1)

    def test_blank_post_does_not_create_post(self):
        form = PostModelForm({"title": "title", "content": ""})
        if form.is_valid():
            form.save(author=self.author)
        self.assertEqual(Post.objects.count(), 0)

    def test_form_save_returns_the_post_object(self):
        form = PostModelForm({"title": "title", "content": "content"})
        post = None
        if form.is_valid():
            post = form.save(author=self.author)
        self.assertEqual(post, Post.objects.first())

    def test_saves_author_with_post(self):
        form = PostModelForm({"title": "title", "content": "content"})
        post = None
        if form.is_valid():
            post = form.save(author=self.author)
        self.assertEqual(post.author, self.author)