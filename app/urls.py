from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path("register", views.register),
    path("login", views.login_view),
    path("logout", views.logout_view),
    path("login/check", views.login_check),
    path("deposit", views.deposit),
    path("pickup", views.pickup),
    path("deposit/list", views.deposit_list),
    path("pickup/list", views.pickup_list),
    path("open/list", views.open_list),
    path("clear", views.clear),
    path("test", views.test)
]
