from django.test import TestCase
from blogger.models import Post
from django.urls import reverse


class PostModelTest(TestCase):
    def test_valid_data_creates_post(self):
        Post.objects.create(content="content")
        self.assertEqual(Post.objects.count(), 1)

    def test_posts_are_ordered_by_creation_date(self):
        post1 = Post.objects.create(content="content")
        post2 = Post.objects.create(content="content")
        self.assertEqual(Post.objects.first(), post2)

    def test_modified_date_is_changed_on_modification(self):
        post = Post.objects.create(content="content")
        pre_modification = post.modified
        post.content = "other content"
        post.save()
        post_modification = post.modified
        self.assertLess(pre_modification, post_modification)

    def test_get_absolute_url_returns_slugified_url(self):
        post = Post.objects.create(title="My title", content="content")
        self.assertEqual(post.get_absolute_url(), f"/blogger/posts/{post.title_slug}/")

    def test_slugified_title_is_saved_on_creation(self):
        post = Post.objects.create(title="My title", content="content")
        self.assertEqual(post.title_slug, "my-title")
