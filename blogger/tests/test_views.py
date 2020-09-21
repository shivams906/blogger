from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse
from unittest.mock import patch
from blogger import views
from blogger.forms import PostModelForm
from blogger.models import Post


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


class AddPostViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        found = resolve("/blogger/add/")
        self.assertEqual(found.func, views.add)

    def test_view_returns_a_valid_response(self):
        response = self.client.get("/blogger/add/")
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        response = self.client.get("/blogger/add/")
        self.assertTemplateUsed(response, "blogger/add.html")

    def test_view_contains_form_in_context(self):
        response = self.client.get("/blogger/add/")
        self.assertIn("form", response.context)

    def test_view_returns_correct_form(self):
        response = self.client.get("/blogger/add/")
        self.assertIsInstance(response.context["form"], PostModelForm)

    def test_valid_data_creates_a_post(self):
        self.client.post("/blogger/add/", data={"title": "title", "content": "content"})
        self.assertEqual(Post.objects.count(), 1)

    def test_valid_post_redirects_to_post_page(self):
        response = self.client.post(
            "/blogger/add/", data={"title": "title", "content": "content"}
        )
        self.assertRedirects(response, "/blogger/posts/title/")


class PostViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        post = Post.objects.create(title="My title", content="content")
        found = resolve(f"/blogger/posts/{post.title_slug}/")
        self.assertEqual(found.func, views.view_post)

    def test_view_returns_a_valid_response(self):
        post = Post.objects.create(title="My title", content="content")
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        post = Post.objects.create(title="My title", content="content")
        response = self.client.get(f"/blogger/posts/{post.title_slug}/")
        self.assertTemplateUsed(response, "blogger/view_post.html")