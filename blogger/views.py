from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "blogger/index.html")


def add(request):
    return render(request, "blogger/add.html")