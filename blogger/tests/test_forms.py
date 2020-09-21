from django.test import TestCase
from blogger.models import Post
from blogger.forms import PostModelForm


class PostModelFormTest(TestCase):
    def test_valid_data_creates_post(self):
        form = PostModelForm({"title": "title", "content": "content"})
        if form.is_valid():
            form.save()
        self.assertEqual(Post.objects.count(), 1)

    def test_blank_post_does_not_create_post(self):
        form = PostModelForm({"content": ""})
        if form.is_valid():
            form.save()
        self.assertEqual(Post.objects.count(), 0)

    def test_form_save_returns_the_post_object(self):
        form = PostModelForm({"content": "content"})
        post = None
        if form.is_valid():
            post = form.save()
        self.assertEqual(post, Post.objects.first())