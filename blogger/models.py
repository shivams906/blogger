from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.utils import IntegrityError

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    title_slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogger:view_post", args=[self.title_slug])

    def save(self, *args, **kwargs):
        if self.title == "":
            raise IntegrityError("No title provided")
        if self.content == "":
            raise IntegrityError("No content provided")
        self.title_slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    comment_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.comment_text


@receiver(post_save, sender=User)
def create_author(sender, **kwargs):
    if kwargs["created"]:
        Author.objects.create(user=kwargs["instance"])
