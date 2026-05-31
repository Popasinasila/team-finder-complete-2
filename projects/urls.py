from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.project_list, name="project_list"),
    path("<int:pk>/", views.project_detail, name="project_detail"),
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/edit/", views.edit_project, name="edit_project"),
    path("<int:pk>/complete/", views.complete_project, name="complete_project"),
    path("favorites/", views.favorites, name="favorites"),
    path("<int:pk>/toggle-favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("<int:pk>/join/", views.join_project, name="join_project"),
]
