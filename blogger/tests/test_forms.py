from django.test import TestCase
from django.contrib.auth import get_user_model
from blogger.models import Post, Author, Comment
from blogger.forms import PostModelForm, CommentModelForm

User = get_user_model()


class PostModelFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user", password="top_secret")
        cls.author = Author.objects.get(user=user)

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

    def test_updates_the_post_if_already_exists(self):
        post = Post.objects.create(title="title", content="content", author=self.author)

        form = PostModelForm(
            {"title": "my title", "content": "my content"}, instance=post
        )
        changed_post = None
        if form.is_valid():
            changed_post = form.save(author=self.author)

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post, changed_post)


class CommentModelFormTest(TestCase):
    def test_valid_data_creates_comment(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        form = CommentModelForm({"comment_text": "comment"})
        if form.is_valid():
            form.save(post, author)
        self.assertEqual(Comment.objects.count(), 1)

    def test_empty_comment_is_not_saved(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        form = CommentModelForm({"comment_text": ""})
        if form.is_valid():
            form.save(post, author)
        self.assertIn("comment_text", form.errors)
        self.assertIn("This field is required.", form.errors["comment_text"])
        self.assertEqual(Comment.objects.count(), 0)