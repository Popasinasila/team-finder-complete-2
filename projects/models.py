from django.conf import settings
from django.db import models


class Project(models.Model):
    STATUS_CHOICES = [
        ("open", "Открыт"),
        ("in_progress", "В работе"),
        ("completed", "Завершён"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="joined_projects",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FavoriteProject(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="favorited_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "project")

    def __str__(self):
        return f"{self.user} → {self.project}"
