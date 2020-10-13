from django.test import TestCase
from django.contrib.auth import get_user_model
from blogger.models import Post, Author, Comment
from django.urls import reverse

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user", password="top_secret")
        cls.author = Author.objects.get(user=user)

    def test_valid_data_creates_post(self):
        Post.objects.create(content="content", author=self.author)
        self.assertEqual(Post.objects.count(), 1)

    def test_posts_are_ordered_by_creation_date(self):
        post1 = Post.objects.create(
            title="title1", content="content", author=self.author
        )
        post2 = Post.objects.create(
            title="title2", content="content", author=self.author
        )
        self.assertEqual(Post.objects.first(), post2)

    def test_modified_date_is_changed_on_modification(self):
        post = Post.objects.create(content="content", author=self.author)
        pre_modification = post.modified
        post.content = "other content"
        post.save()
        post_modification = post.modified
        self.assertLess(pre_modification, post_modification)

    def test_get_absolute_url_returns_slugified_url(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        self.assertEqual(post.get_absolute_url(), f"/blogger/posts/{post.title_slug}/")

    def test_slugified_title_is_saved_on_creation(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        self.assertEqual(post.title_slug, "my-title")


class AuthorModelTest(TestCase):
    def test_author_object_is_created_automatically_on_user_creation(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.first()
        self.assertIsNotNone(author)
        self.assertEqual(author.user, user)

    def test_author_object_is_displayed_as_username(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        self.assertEqual(str(author), author.user.username)


class CommentModelTest(TestCase):
    def test_valid_data_creates_comment(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        Comment.objects.create(comment_text="comment", post=post, author=author)
        self.assertEqual(Comment.objects.count(), 1)

    def test_timestamp_is_added_automatically(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        comment = Comment.objects.create(
            comment_text="comment", post=post, author=author
        )
        self.assertIsNotNone(comment.created)

    def test_string_representation(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        comment = Comment.objects.create(
            comment_text="comment", post=post, author=author
        )
        self.assertEqual(str(comment), comment.comment_text)

    def test_comments_are_ordered_by_creation_date(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        comment1 = Comment.objects.create(
            comment_text="comment", post=post, author=author
        )
        comment2 = Comment.objects.create(
            comment_text="comment", post=post, author=author
        )
        comments = Comment.objects.all()
        self.assertEqual(comment1, comments[0])
        self.assertEqual(comment2, comments[1])