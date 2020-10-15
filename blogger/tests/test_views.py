from django.test import TestCase
from django.urls import resolve, reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from blogger import views
from blogger.forms import PostModelForm, CommentModelForm
from blogger.models import Post, Author, Comment


User = get_user_model()


class IndexViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        found = resolve(reverse("blogger:index"))
        self.assertEqual(found.func, views.index)

    def test_view_returns_a_valid_response(self):
        response = self.client.get(reverse("blogger:index"))
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("blogger:index"))
        self.assertTemplateUsed(response, "blogger/index.html")

    def test_passes_all_posts_as_context(self):
        user1 = User.objects.create(username="user1", password="top_secret")
        author1 = Author.objects.get(user=user1)
        post1 = Post.objects.create(title="title1", content="content", author=author1)
        user2 = User.objects.create(username="user2", password="top_secret")
        author2 = Author.objects.get(user=user2)
        post2 = Post.objects.create(title="title2", content="content", author=author2)

        response = self.client.get(reverse("blogger:index"))

        self.assertIn("page_obj", response.context)
        self.assertEqual(len(response.context["page_obj"]), 2)
        self.assertIn(post1, response.context["page_obj"])
        self.assertIn(post2, response.context["page_obj"])

    def test_posts_context_object_is_paginated(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        for i in range(11):
            post = Post.objects.create(
                title=f"title{i}", content="content", author=author
            )
        response = self.client.get(reverse("blogger:index"))
        self.assertIn("page_obj", response.context)
        self.assertEqual(len(response.context["page_obj"]), 10)


class AddPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user", password="top_secret")

    def test_url_resolves_to_correct_view_function(self):
        found = resolve(reverse("blogger:add_post"))
        self.assertEqual(found.func, views.add)

    def test_view_returns_a_valid_response(self):
        response = self.client.get(reverse("blogger:add_post"))
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("blogger:add_post"))
        self.assertTemplateUsed(response, "blogger/add.html")

    def test_view_contains_form_in_context(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("blogger:add_post"))
        self.assertIn("form", response.context)

    def test_view_returns_correct_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("blogger:add_post"))
        self.assertIsInstance(response.context["form"], PostModelForm)

    def test_valid_data_creates_a_post(self):
        self.client.force_login(self.user)

        self.client.post(
            reverse("blogger:add_post"), data={"title": "title", "content": "content"}
        )
        self.assertEqual(Post.objects.count(), 1)

    def test_valid_post_redirects_to_post_page(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("blogger:add_post"), data={"title": "title", "content": "content"}
        )
        self.assertRedirects(response, "/blogger/posts/title/")

    def test_current_user_is_saved_as_author(self):
        self.client.force_login(self.user)

        self.client.post(
            reverse("blogger:add_post"), data={"title": "title", "content": "content"}
        )
        post = Post.objects.first()

        self.assertIsInstance(post.author, Author)
        self.assertEqual(post.author.user, self.user)

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        response = self.client.get(reverse("blogger:add_post"))
        self.assertRedirects(response, "/accounts/login/?next=/blogger/add/")


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="user", password="top_secret")
        cls.author = Author.objects.get(user=user)

    def test_url_resolves_to_correct_view_function(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        found = resolve(reverse("blogger:view_post", args=(post.title_slug,)))
        self.assertEqual(found.func, views.view_post)

    def test_view_returns_a_valid_response(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(
            reverse("blogger:view_post", args=(post.title_slug,))
        )
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(
            reverse("blogger:view_post", args=(post.title_slug,))
        )
        self.assertTemplateUsed(response, "blogger/view_post.html")

    def test_context_contains_post_object(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(
            reverse("blogger:view_post", args=(post.title_slug,))
        )
        self.assertIn("post", response.context)

    def test_context_post_object_is_correct_one(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        response = self.client.get(
            reverse("blogger:view_post", args=(post.title_slug,))
        )
        self.assertEqual(post, response.context["post"])

    def test_context_contains_post_comments(self):
        post = Post.objects.create(
            title="My title", content="content", author=self.author
        )
        comment = Comment.objects.create(
            comment_text="comment", post=post, author=self.author
        )
        response = self.client.get(
            reverse("blogger:view_post", args=(post.title_slug,))
        )
        self.assertIn("comments", response.context)
        self.assertIn(comment, response.context["comments"])


class AuthorViewTest(TestCase):
    def test_url_resolves_to_correct_view_function(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        found = resolve(reverse("blogger:view_blogger", args=(author,)))
        self.assertEqual(found.func, views.view_blogger)

    def test_view_returns_a_valid_response(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        response = self.client.get(reverse("blogger:view_blogger", args=(author,)))
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        response = self.client.get(reverse("blogger:view_blogger", args=(author,)))
        self.assertTemplateUsed(response, "blogger/view_blogger.html")

    def test_view_returns_correct_author_object_in_context(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        response = self.client.get(reverse("blogger:view_blogger", args=(author,)))
        self.assertIn("author", response.context)
        self.assertEqual(response.context["author"], author)

    def test_invalid_author_name_returns_appropriate_response(self):
        response = self.client.get(f"/blogger/bloggers/user/")
        self.assertContains(response, "There is no author by that username")

    def test_view_returns_correct_posts_object_in_context(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        post = Post.objects.create(title="title", content="content", author=author)
        response = self.client.get(reverse("blogger:view_blogger", args=(author,)))
        self.assertIn("posts", response.context)
        self.assertIn(post, response.context["posts"])

    def test_invalid_author_with_no_posts_returns_appropriate_response(self):
        user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=user)
        response = self.client.get(reverse("blogger:view_blogger", args=(author,)))
        self.assertContains(response, f"There are no posts written by {author}")


class EditPostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=cls.user)
        cls.post = Post.objects.create(title="title", content="content", author=author)

    def test_url_resolves_to_correct_view_function(self):
        self.client.force_login(self.user)
        found = resolve(reverse("blogger:edit_post", args=(self.post.title_slug,)))
        self.assertEqual(found.func, views.edit_post)

    def test_view_returns_a_valid_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:edit_post", args=(self.post.title_slug,))
        )
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:edit_post", args=(self.post.title_slug,))
        )
        self.assertTemplateUsed(response, "blogger/add.html")

    def test_view_passes_correct_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:edit_post", args=(self.post.title_slug,))
        )
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], PostModelForm)

    def test_view_passes_bound_form(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:edit_post", args=(self.post.title_slug,))
        )
        form = response.context["form"]
        self.assertEqual(form.instance, self.post)

    def test_post_updates_data(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("blogger:edit_post", args=(self.post.title_slug,)),
            data={"title": "my title", "content": "my content"},
        )
        changed_post = Post.objects.get(id=self.post.id)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual("my title", changed_post.title)
        self.assertEqual("my content", changed_post.content)

    def test_valid_post_redirects_to_post_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("blogger:edit_post", args=(self.post.title_slug,)),
            data={"title": "my title", "content": "my content"},
        )
        self.assertRedirects(response, "/blogger/posts/my-title/")

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        response = self.client.post(
            reverse("blogger:edit_post", args=(self.post.title_slug,)),
            data={"title": "my title", "content": "my content"},
        )
        self.assertRedirects(
            response, "/accounts/login/?next=/blogger/posts/title/edit/"
        )

    def test_users_other_than_post_author_are_shown_the_appropriate_response(
        self,
    ):
        user2 = User.objects.create(username="user2", password="top_secret")
        self.client.force_login(user2)
        response = self.client.get(
            reverse("blogger:edit_post", args=(self.post.title_slug,))
        )
        self.assertNotIn("form", response.context)
        self.assertContains(response, "You cannot edit this post")


class DeletePostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=cls.user)
        cls.post = Post.objects.create(title="title", content="content", author=author)

    def test_url_resolves_to_correct_view_function(self):
        self.client.force_login(self.user)
        found = resolve(reverse("blogger:delete_post", args=(self.post.title_slug,)))
        self.assertEqual(found.func, views.delete_post)

    def test_view_returns_a_valid_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertTemplateUsed(response, "blogger/delete_post.html")

    def test_view_passes_post_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertIn("post", response.context)
        self.assertEqual(self.post, response.context["post"])

    def test_asks_for_confirmation_before_deletion(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertContains(response, "Are you sure you want to delete title?")

    def test_confirmation_deletes_post(self):
        self.client.force_login(self.user)
        self.client.post(reverse("blogger:delete_post", args=(self.post.title_slug,)))
        self.assertEqual(Post.objects.count(), 0)

    def test_confirmation_redirects_to_home_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertRedirects(response, "/blogger/")

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertRedirects(
            response, "/accounts/login/?next=/blogger/posts/title/delete/"
        )

    def test_users_other_than_post_author_are_shown_the_appropriate_response(self):
        user2 = User.objects.create(username="user2", password="top_secret")
        self.client.force_login(user2)
        response = self.client.get(
            reverse("blogger:delete_post", args=(self.post.title_slug,))
        )
        self.assertNotIn("post", response.context)
        self.assertContains(response, "You cannot delete this post")


class AddCommentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="user", password="top_secret")
        author = Author.objects.get(user=cls.user)
        cls.post = Post.objects.create(title="title", content="content", author=author)

    def test_url_resolves_to_correct_view_function(self):
        found = resolve(reverse("blogger:add_comment", args=(self.post.title_slug,)))
        self.assertEqual(found.func, views.add_comment)

    def test_view_returns_a_valid_response(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:add_comment", args=(self.post.title_slug,))
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:add_comment", args=(self.post.title_slug,))
        )
        self.assertTemplateUsed(response, "blogger/add_comment.html")

    def test_view_passes_correct_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("blogger:add_comment", args=(self.post.title_slug,))
        )
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CommentModelForm)

    def test_valid_post_saves_comment(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("blogger:add_comment", args=(self.post.title_slug,)),
            data={"comment_text": "comment"},
        )
        self.assertEqual(Comment.objects.count(), 1)

    def test_valid_post_redirects_to_post_page(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("blogger:add_comment", args=(self.post.title_slug,)),
            data={"comment_text": "comment"},
        )
        self.assertRedirects(response, self.post.get_absolute_url())

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        response = self.client.post(
            reverse("blogger:add_comment", args=(self.post.title_slug,)),
            data={"comment_text": "comment"},
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/blogger/posts/{self.post.title_slug}/comment/",
        )
