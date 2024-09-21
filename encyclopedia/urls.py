from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("search_result", views.search_result, name="search_result"),
    path("NewPage", views.new_page, name="NewPage"),
    path("EditPage/<str:edt_title>", views.edit_page, name="EditPage"),
    path("random", views.random_page, name="random")
]


