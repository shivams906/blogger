from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from blogger.forms import PostModelForm
from blogger.models import Post, Author


def index(request):
    posts = Post.objects.all()
    return render(request, "blogger/index.html", {"posts": posts})


@login_required
def add(request):
    author = get_or_create_author(request.user)
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save(author=author)
            return redirect(post)
    else:
        form = PostModelForm()
    return render(request, "blogger/add.html", {"form": form})


def view_post(request, title):
    post = Post.objects.get(title_slug=title)
    return render(request, "blogger/view_post.html", {"post": post})


def get_or_create_author(user):
    try:
        author = Author.objects.get(user=user)
    except Author.DoesNotExist:
        author = Author.objects.create(user=user)
    return author
