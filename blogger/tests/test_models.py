from django.test import TestCase
from django.contrib.auth import get_user_model
from blogger.models import Post, Author
from django.urls import reverse

User = get_user_model()


class PostModelTest(TestCase):
    def test_valid_data_creates_post(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        Post.objects.create(content="content", author=author)
        self.assertEqual(Post.objects.count(), 1)

    def test_posts_are_ordered_by_creation_date(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        post1 = Post.objects.create(content="content", author=author)
        post2 = Post.objects.create(content="content", author=author)
        self.assertEqual(Post.objects.first(), post2)

    def test_modified_date_is_changed_on_modification(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        post = Post.objects.create(content="content", author=author)
        pre_modification = post.modified
        post.content = "other content"
        post.save()
        post_modification = post.modified
        self.assertLess(pre_modification, post_modification)

    def test_get_absolute_url_returns_slugified_url(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        post = Post.objects.create(title="My title", content="content", author=author)
        self.assertEqual(post.get_absolute_url(), f"/blogger/posts/{post.title_slug}/")

    def test_slugified_title_is_saved_on_creation(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        post = Post.objects.create(title="My title", content="content", author=author)
        self.assertEqual(post.title_slug, "my-title")


class AuthorModelTest(TestCase):
    def test_author_object_is_displayed_as_username(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        self.assertEqual(str(author), author.user.username)