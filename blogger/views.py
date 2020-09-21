from django.shortcuts import render, redirect
from django.http import HttpResponse
from blogger.forms import PostModelForm


def index(request):
    return render(request, "blogger/index.html")


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
    return render(request, "blogger/view_post.html")
