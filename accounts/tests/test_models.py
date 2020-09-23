from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import User


class UserModelTest(TestCase):
    def test_User_is_the_auth_user_model(self):
        self.assertEqual(User, get_user_model())

    def test_can_create_user_with_username_and_password(self):
        User.objects.create_user(username="user1", password="top_secret")
        self.assertEqual(User.objects.count(), 1)