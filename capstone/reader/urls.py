from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:sort>/<int:current_count>", views.index, name="index_sort"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("story/<str:id>", views.story, name="story"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("reader/<str:id>/<str:type>", views.reader, name="reader"),
    path("submit", views.submit, name="submit"),
    path("intro_edit", views.intro_edit, name="intro_edit"),
    path("category/<str:type>/<str:query>", views.category, name="category")
]
