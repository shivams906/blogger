from django.urls import path, re_path
from blogger import views

app_name = "blogger"
urlpatterns = [
    path("", views.index, name="index"),
    path("posts/add/", views.add, name="add_post"),
    re_path(r"^posts/([\w\d\-]+)/$", views.view_post, name="view_post"),
    re_path(r"^posts/([\w\d\-]+)/edit/$", views.edit_post, name="edit_post"),
    re_path(r"^posts/([\w\d\-]+)/delete/$", views.delete_post, name="delete_post"),
    re_path(r"^posts/([\w\d\-]+)/comment/$", views.add_comment, name="add_comment"),
    re_path(r"^bloggers/([\w\d\-]+)/$", views.view_blogger, name="view_blogger"),
]
