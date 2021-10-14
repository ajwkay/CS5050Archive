from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:id>', views.listing, name="listing"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('<str:cat>/categories', views.categories, name="categories"),
    path("categorylist", views.categorylist, name="categorylist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creator", views.creator, name="creator"),
    path("<int:id>/editor", views.editor, name="editor"),
    path("<int:id>/close", views.close, name="close")
]
