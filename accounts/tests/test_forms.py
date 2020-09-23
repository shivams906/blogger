from django.test import TestCase
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationFormTest(TestCase):
    def test_form_creates_a_user_with_user_and_password(self):
        form = CustomUserCreationForm(
            {"username": "user1", "password1": "top_secret", "password2": "top_secret"}
        )
        if form.is_valid():
            form.save()
        self.assertEqual(User.objects.count(), 1)

    def test_form_fields_contain_first_and_last_name_and_username(self):
        self.assertEqual(
            CustomUserCreationForm.Meta.fields, ("username", "first_name", "last_name")
        )
