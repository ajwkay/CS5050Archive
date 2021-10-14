from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:name>', views.page, name="Page"),
    path('results/', views.results, name="Results"),
    path('pageEdit/', views.pageEdit, name="pageEdit")
]
