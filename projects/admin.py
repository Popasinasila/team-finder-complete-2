from django.contrib import admin
from .models import Project, FavoriteProject


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "author__email")
    ordering = ("-created_at",)


@admin.register(FavoriteProject)
class FavoriteProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "project", "created_at")
