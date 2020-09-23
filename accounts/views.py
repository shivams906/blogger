from django.shortcuts import render, redirect
from accounts.forms import CustomUserCreationForm


def signup(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "registration/signup.html", {"form": form})
