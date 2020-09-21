from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Post(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    title_slug = models.SlugField()

    class Meta:
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("blogger:view_post", args=[self.title_slug])

    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        return super().save(*args, **kwargs)