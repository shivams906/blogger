from django.urls import path, re_path
from blogger import views

app_name = "blogger"
urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    re_path(r"^posts/([\w\d\-]+)/$", views.view_post, name="view_post"),
]
