from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blogger.models import Post, Author, Comment

from faker import Faker
from faker.providers import person

User = get_user_model()

fake = Faker()
Faker.seed(0)
fake.add_provider(person)


class Command(BaseCommand):
    def _create_authors(self):
        self.authors = []
        for _ in range(5):
            user = User.objects.create(
                username=fake.first_name(), password="top_secret"
            )
            author = Author.objects.get(user=user)
            self.authors.append(author)

    def _create_posts(self):
        self.posts = []
        for author in self.authors:
            for _ in range(5):
                post = Post.objects.create(
                    title=fake.text(),
                    content="\n".join(
                        [("".join([fake.text() for _ in range(5)])) for _ in range(5)]
                    ),
                    author=author,
                )
                self.posts.append(post)

    def _create_comments(self):
        for post in self.posts:
            for author in self.authors:
                Comment.objects.create(
                    comment_text=fake.text(), post=post, author=author
                )

    def handle(self, *args, **options):
        self._create_authors()
        self._create_posts()
        self._create_comments()
