from django.test import TestCase
from django.urls import resolve
from accounts.views import signup
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpTest(TestCase):
    def test_signup_url_reolves_to_signup_function(self):
        found = resolve("/accounts/signup/")
        self.assertEqual(found.func, signup)

    def test_signup_uses_the_correct_template(self):
        response = self.client.get("/accounts/signup/")
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_passes_the_signup_form_in_context(self):
        response = self.client.get("/accounts/signup/")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_valid_POST_creates_new_user(self):
        self.client.post(
            "/accounts/signup/",
            {"username": "user1", "password1": "top_secret", "password2": "top_secret"},
        )
        self.assertEqual(User.objects.count(), 1)

    def test_valid_POST_redirects_to_login_page(self):
        response = self.client.post(
            "/accounts/signup/",
            {"username": "user1", "password1": "top_secret", "password2": "top_secret"},
        )
        self.assertRedirects(response, "/accounts/login/")


class LoginTest(TestCase):
    def test_login_redirects_to_home_page(self):
        self.client.post(
            "/accounts/signup/",
            {"username": "user1", "password1": "top_secret", "password2": "top_secret"},
        )
        response = self.client.post(
            "/accounts/login/",
            {"username": "user1", "password": "top_secret"},
        )
        self.assertRedirects(response, "/blogger/")


class LogoutTest(TestCase):
    def test_logout_redirects_to_home_page(self):
        self.client.post(
            "/accounts/signup/",
            {"username": "user1", "password1": "top_secret", "password2": "top_secret"},
        )
        self.client.post(
            "/accounts/login/",
            {"username": "user1", "password": "top_secret"},
        )
        response = self.client.get("/accounts/logout/")
        self.assertRedirects(response, "/blogger/")
