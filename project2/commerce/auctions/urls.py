from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name = "create_listing"),
    path("category/<str:cat>", views.cat, name="cat"),
    path("category", views.category, name = "category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("<int:id>/watchlist", views.list, name="list"),
    path("watchlist", views.watchlist, name="watchlist")
]
