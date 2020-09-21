from django.test import TestCase
from django.urls import resolve
from django.http import HttpResponse
from blogger import views


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
