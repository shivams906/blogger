from django.urls import path
from blogger import views

app_name = "blogger"
urlpatterns = [
    path("", views.index, name="index"),
]
