from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from blogger import views
from blogger.forms import PostModelForm
from blogger.models import Post, Author


User = get_user_model()


class IndexViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        found = resolve("/blogger/")
        self.assertEqual(found.func, views.index)

    def test_view_returns_a_valid_response(self):
        response = self.client.get("/blogger/")
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        response = self.client.get("/blogger/")
        self.assertTemplateUsed(response, "blogger/index.html")

    def test_passes_all_posts_as_context(self):
        user1 = User.objects.create(username="user1", password="top_secret")
        author1 = Author.objects.create(user=user1)
        post1 = Post.objects.create(title="title", content="content", author=author1)
        user2 = User.objects.create(username="user2", password="top_secret")
        author2 = Author.objects.create(user=user2)
        post2 = Post.objects.create(title="title", content="content", author=author2)

        response = self.client.get("/blogger/")

        self.assertIn("posts", response.context)
        self.assertEqual(len(response.context["posts"]), 2)
        self.assertIn(post1, response.context["posts"])
        self.assertIn(post2, response.context["posts"])


class AddPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user", password="top_secret")

    def test_url_resolves_to_correct_view_function(self):
        found = resolve("/blogger/add/")
        self.assertEqual(found.func, views.add)

    def test_view_returns_a_valid_response(self):
        response = self.client.get("/blogger/add/")
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get("/blogger/add/")
        self.assertTemplateUsed(response, "blogger/add.html")

    def test_view_contains_form_in_context(self):
        self.client.force_login(self.user)

        response = self.client.get("/blogger/add/")
        self.assertIn("form", response.context)

    def test_view_returns_correct_form(self):
        self.client.force_login(self.user)

        response = self.client.get("/blogger/add/")
        self.assertIsInstance(response.context["form"], PostModelForm)

    def test_valid_data_creates_a_post(self):
        self.client.force_login(self.user)

        self.client.post("/blogger/add/", data={"title": "title", "content": "content"})
        self.assertEqual(Post.objects.count(), 1)

    def test_valid_post_redirects_to_post_page(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/blogger/add/", data={"title": "title", "content": "content"}
        )
        self.assertRedirects(response, "/blogger/posts/title/")

    def test_current_user_is_saved_as_author(self):
        self.client.force_login(self.user)

        self.client.post("/blogger/add/", data={"title": "title", "content": "content"})
        post = Post.objects.first()

        self.assertIsInstance(post.author, Author)
        self.assertEqual(post.author.user, self.user)

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        response = self.client.get("/blogger/add/")
        self.assertRedirects(response, "/accounts/login/?next=/blogger/add/")


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user", password="top_secret")
        cls.author = Author.objects.create(user=user)

    def test_url_resolves_to_correct_view_function(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        found = resolve(f"/blogger/posts/{post.title_slug}/")
        self.assertEqual(found.func, views.view_post)

    def test_view_returns_a_valid_response(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertTemplateUsed(response, "blogger/view_post.html")

    def test_context_contains_post_object(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertIn("post", response.context)

    def test_context_post_object_is_correct_one(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertEqual(post, response.context["post"])


class AuthorViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        found = resolve(f"/blogger/bloggers/{author.user.username}/")
        self.assertEqual(found.func, views.view_blogger)

    def test_view_returns_a_valid_response(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        response = self.client.get(f"/blogger/bloggers/{author.user.username}/")
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        response = self.client.get(f"/blogger/bloggers/{author.user.username}/")
        self.assertTemplateUsed(response, "blogger/view_blogger.html")

    def test_view_returns_correct_author_object_in_context(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.create(user=user)
        response = self.client.get(f"/blogger/bloggers/{author.user.username}/")
        self.assertIn("author", response.context)
        self.assertEqual(response.context["author"], author)

    def test_invalid_author_name_returns_appropriate_response(self):
        response = self.client.get(f"/blogger/bloggers/user/")
        self.assertContains(response, "There is no author by that username")
