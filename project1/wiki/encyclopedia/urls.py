from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search, name="search"),
    path('editor', views.editor, name="editor"),
    path('random', views.random, name="random"),
    path('<str:title>/mod', views.mod, name="mod"),
    path("<str:title>",views.wiki_entry,name="wiki_entry")
]
