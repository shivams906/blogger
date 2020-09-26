from django.shortcuts import render, redirect
from django.http import HttpResponse
from blogger.forms import PostModelForm
from blogger.models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, "blogger/index.html", {"posts": posts})


def add(request):
    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect(post)
    else:
        form = PostModelForm()
    return render(request, "blogger/add.html", {"form": form})


def view_post(request, title):
    post = Post.objects.get(title_slug=title)
    return render(request, "blogger/view_post.html", {"post": post})
