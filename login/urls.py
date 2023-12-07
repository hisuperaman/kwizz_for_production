from django.urls import path, include
from . import views

app_name = "login"
urlpatterns = [
    path("", view=views.index, name="index"),

    path("login/", view=views.login, name="login"),
    path("callback/", view=views.callback, name="callback"),
    path("logout/", view=views.logout, name="logout"),

    path("welcome/", view=views.welcome, name="welcome"),
    path("username_exists/", view=views.username_exists, name="username_exists"),
]