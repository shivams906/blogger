from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from blogger.forms import PostModelForm, CommentModelForm
from blogger.models import Post, Author

User = get_user_model()


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


@login_required
def edit_post(request, title):
    post = Post.objects.get(title_slug=title)
    if post.author.user == request.user:
        if request.method == "POST":
            form = PostModelForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(post.author)
                return redirect(post)
        else:
            form = PostModelForm(instance=post)
        return render(request, "blogger/add.html", {"form": form})
    else:
        return render(request, "blogger/add.html")


def view_post(request, title):
    post = Post.objects.get(title_slug=title)
    comments = post.comment_set.all()
    return render(
        request, "blogger/view_post.html", {"post": post, "comments": comments}
    )


@login_required
def delete_post(request, title):
    post = Post.objects.get(title_slug=title)
    if post.author.user == request.user:
        if request.method == "POST":
            post.delete()
            return redirect(reverse("blogger:index"))
        return render(request, "blogger/delete_post.html", {"post": post})
    else:
        return render(request, "blogger/delete_post.html")


@login_required
def add_comment(request, title):
    if request.method == "POST":
        post = Post.objects.get(title_slug=title)
        author = get_or_create_author(request.user)
        form = CommentModelForm(request.POST)
        if form.is_valid():
            form.save(post=post, author=author)
            return redirect(post)
    else:
        form = CommentModelForm()
    return render(request, "blogger/add_comment.html", {"form": form})


def view_blogger(request, username):
    try:
        user = User.objects.get(username=username)
        author = get_or_create_author(user)
        posts = Post.objects.filter(author=author)
    except User.DoesNotExist:
        author = None
        posts = None
    return render(
        request, "blogger/view_blogger.html", {"author": author, "posts": posts}
    )


def get_or_create_author(user):
    try:
        author = Author.objects.get(user=user)
    except Author.DoesNotExist:
        author = Author.objects.create(user=user)
    return author
