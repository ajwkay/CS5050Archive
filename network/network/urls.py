
from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("feed", views.feed, name="feed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('like', views.like, name="like"),
    path('edit', views.edit, name="edit"),
]
