from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/<int:pk>/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("list/", views.users_list, name="users_list"),
    path("password/", views.change_password, name="change_password"),
]
